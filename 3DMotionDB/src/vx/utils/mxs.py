'''
Created on Feb 9, 2014

@author: Jing
'''
import numpy
from pymaxwell import *

import utils as Utils


from xml.etree.ElementTree import Element, SubElement #, ElementTree, dump, tostring

class CObjectType:        
    Group, Instance, Geometry, Unkown=range(4)


def getObjectType(obj):
    
    objType = CObjectType.Group
    isMeshed, ok = obj.isMesh()
    if isMeshed == 0: # this object is not meshed
        isInstance, ok = obj.isInstance()
        if isInstance == 1:
            objType = CObjectType.Instance
        else:
            objType = CObjectType.Unkown
    else: # this object is meshed
        nTriangles, ok = obj.getTrianglesCount()
        if nTriangles > 0:
            return CObjectType.Geometry
        else:
            return CObjectType.Unkown
        
    return objType


def getObjectVertices(obj, step=0):
    '''
    return  the world/global coordinates of all vertices
    '''
    
    objType = getObjectType(obj)
    assert objType == CObjectType.Instance or objType== CObjectType.Geometry
    
    # get the transformation matrix 
    base, ok = obj.getWorldTransform()
    u = (base.xAxis[0], base.xAxis[1], base.xAxis[2])
    v = (base.yAxis[0], base.yAxis[1], base.yAxis[2])
    w = (base.zAxis[0], base.zAxis[1], base.zAxis[2])
    o = (base.origin[0], base.origin[1], base.origin[2])
    transfMtx = numpy.array([u, v, w, o], dtype=numpy.float32)
    
    # get the coordinates of all vertices
    realObj = obj
    if objType == CObjectType.Instance:
        realObj = obj.getInstanced()

    nVertices, ok = realObj.getVerticesCount()
    points = numpy.ones((nVertices,4), dtype=numpy.float32)
    for vId in range(nVertices):
        v, ok = realObj.getVertex(vId, step)
        points[vId][0] = v[0]
        points[vId][1] = v[1]
        points[vId][2] = v[2]
        
    # transform the local coordinates to global coordinates
    points = numpy.dot(points, transfMtx)
    
    return points

def getObjectTriangles(obj):

    objType = getObjectType(obj)
    assert objType == CObjectType.Instance or objType== CObjectType.Geometry

    realObj = obj
    if objType == CObjectType.Instance:
        realObj = obj.getInstanced()
        
    nTriangles, ok = realObj.getTrianglesCount()
    faces = numpy.zeros((nTriangles, 3), dtype=numpy.uint32)
    for tId in range(nTriangles):
        triangle = realObj.getTriangle(tId)
        faces[tId][0] = triangle[0]
        faces[tId][1] = triangle[1]
        faces[tId][2] = triangle[2]
        
    return faces

def getObject(scene, name):
    obj = scene.getObject(name)
    return obj

def getObjectTrianglesByMat(obj, matName):
    triIds = []
    matName = matName.lower()
    nTriangles, ok = obj.getTrianglesCount()
    for i in range(nTriangles):
        mat, ok = obj.getTriangleMaterial(i)
        if ok and mat.getName().lower() == matName:
            triIds.append(i)
    
    return triIds



def getObjectGeometris(scene):
    '''
    Method: GetObjectGeometris(Cmaxwell scene) -> (list pointsList, list facesList, list namesList)
    '''
    pointsList = []
    facesList = []
    namesList = []
    
    # iterator each object in the scene
    it = CmaxwellObjectIterator()
    curObj = it.first(scene)
    
    while not curObj.isNull():
        
        if not isSkip(curObj):
            points = getObjectVertices(curObj)
            faces =  getObjectTriangles(curObj)
            name, ok =  curObj.getName()
            pointsList.append(points)
            facesList.append(faces)
            namesList.append(name)     
            
        curObj = it.next()
        
    return (pointsList, facesList, namesList)


def setObjectInvisible(obj):

    obj.setHide(True)
    obj.setHideToCamera(True)
    obj.setHideToGI(True)
    obj.setHideToReflectionsRefractions(True)

def isSkip(obj):
    
    objType = getObjectType(obj)
    isNotGeom = not ( (objType == CObjectType.Instance) or  (objType == CObjectType.Geometry) )
    isHidden, ok = obj.getHide()
    isHideToCamera,ok = obj.getHideToCamera()
    
    return (isNotGeom or isHidden or isHideToCamera)


def buildObjectElement(elem, obj):
    
    """
    Method:  BuildObjectElement(xml.etree.ElementTree.SubElement elem, CmaxwellObject obj)
    Description: Add sub-elements to elem. Each sub-element is an attribute of the obj. 
                 If obj is not meshed, the nVertices, nNormals... will be -1.
    """
    
    isInstance, ok = obj.isInstance()
    isMesh, ok = obj.isMesh()

    nVertices = -1
    nNormals = -1
    nTriangles = -1
    nTriangleGroups = -1
    isWorldCoord = -1
    
    if isMesh==1:
        nVertices, ok = obj.getVerticesCount()
        nNormals, ok = obj.getNormalsCount()
        nTriangles, ok = obj.getTrianglesCount()
        nTriangleGroups, ok = obj.getTriangleGroupsCount() 
        isWorldCoord = obj.isInWorldCoordinates()

            
    SubElement(elem, "isInstance").text = repr(isInstance)
    SubElement(elem, "isMesh").text = repr(isMesh)
    SubElement(elem, "isWorldCoord").text = repr(isWorldCoord)
    SubElement(elem, "nVertices").text = repr(nVertices)
    SubElement(elem, "nNormals").text = repr(nNormals)
    SubElement(elem, "nTriangle").text = repr(nTriangles)
    SubElement(elem, "nTriangleGroup").text = repr(nTriangleGroups)
    
    
def exportMxsObjInformation(scene, pzFile):
    info, ok = scene.getSceneInfo()

    # root element
    root = Element("scene")
    root.attrib["path"] = scene.getMxsPath() 
    root.attrib["nObjects"] = repr(info.nObjects)
    root.attrib["nMeshs"] = repr(info.nMeshes)
    root.attrib["nTriangles"] = repr(info.nTriangles)
    

    objElemList = []
    objNameList = []
    
    # iterate all objects
    it = CmaxwellObjectIterator()
    curObj = it.first(scene)
    while not curObj.isNull():
        objName, ok = curObj.getName()
        parent, ok = curObj.getParent()
       
        objNameList.append(objName)
        parentElem = root
        if not parent.isNull():
            parentName, ok = parent.getName()
            parentIdx = objNameList.index(parentName)
            parentElem = objElemList[parentIdx]
        
        objElem = SubElement(parentElem, "object", name=repr(objName))
        buildObjectElement(objElem, curObj)
        objElemList.append(objElem)
        curObj = it.next()
    
    # write the document to a file
    # ElementTree(root).write(pzFile)
    Utils.saveXML(root, pzFile) 
    print "finish export mxs information"



def setStep(mxCamera, step, origin, focalPoint, up, focalLength, fStop, stepTime, focalLengthNeedCorrection):
    step = int(step)
    cvOrigin = Cvector(origin[0], origin[1], origin[2])
    cvUp = Cvector(up[0], up[1], up[2])
    cvFocalPoint = Cvector(float(focalPoint[0]), float(focalPoint[1]), float(focalPoint[2]))
  
    fStop = float(fStop)
    stepTime =float(stepTime)
    
    mxCamera.setStep( step, cvOrigin, cvFocalPoint, cvUp, focalLength, fStop, stepTime, focalLengthNeedCorrection)
    
def readMXS(pzMxs):
    scene = Cmaxwell(mwcallback)
    ok = scene.readMXS(pzMxs)
    if not ok:
        raise "unable to open file: " + pzMxs
    
    return scene

def writeMXS(scene, pzMxs):

    scene.writeMXS(pzMxs)

def exportMxCamerasInfo2XML(pzScene, pzXML):
    scene = readMXS(pzScene)
    cameras = getCamerasInfo(scene)
    root = buildCameraElement(cameras)
    
    return Utils.saveXML(root, pzXML)
    
    
def getCamerasInfo(scene):
    cameras = []
    it = CmaxwellCameraIterator();
    camera = it.first( scene );
    while not camera.isNull():
        values = camera.getValues()
        steps = []
        for iStep in range(values['nSteps']):
            stepInfo = camera.getStep(iStep)
            steps.append(stepInfo)
        cameras.append((values, steps))
        camera = it.next()
    return cameras
        
def buildCameraElement(cameras, root=None):
    if root == None:
        root = Element("cameras")
        
    for camId in range(len(cameras)):
        elem = SubElement(root, "camera")
        
        values = cameras[camId][0]
        steps = cameras[camId][1]
         
        for key, value in values.items():
            SubElement(elem, key).text = str(value)
        
        elemSteps = SubElement(elem, "steps") 
        stepattrs = ("origin", "focalPoint", "up", "focalLength", "fStop", "stepTime", "focalLengthNeedCorrection")
        for iStep in range(len(steps)):
            step = steps[iStep]
            elemStep = SubElement(elemSteps, "step") 
            SubElement(elemStep, "iStep").text = str(iStep)
            SubElement(elemStep, "origin").text = Cvector2Str(step[0])
            SubElement(elemStep, "focalPoint").text = Cvector2Str(step[1])
            SubElement(elemStep, "up").text = Cvector2Str(step[2])
            SubElement(elemStep, "focalLength").text = str(step[3])
            SubElement(elemStep, "fStop").text = str(step[4])
            SubElement(elemStep, "stepTime").text = str(step[5])
            SubElement(elemStep, "focalLengthNeedCorrection").text = str(step[6])
        
    return root
        
def Cvector2Str(v):
    return "{}, {}, {}".format(v.x(), v.y(), v.z())

def createMxObject(scene, objName, points, normals, triangles):
   
    nVertices = len(points)
    nNormals = len(normals)
    nTriangles = len(triangles)
    nPositionsPerVertex = 1
    
    obj = scene.createMesh(objName, nVertices,nNormals,nTriangles,nPositionsPerVertex)
    if obj.isNull():
        raise("Error creating mesh");
    
    
    # Vertices
    ok = True
    for i in range(nVertices):
        pt = points[i]
        mxPt =  Cvector(pt[0], pt[1], pt[2])
        ok  &= obj.setVertex(i, 0, mxPt)
    if not ok:
        raise("Error setting vertices")
    
    
    # Normals
    ok = True
    for i in range(nNormals):
        normal = normals[i]
        mxNormal =  Cvector(float(normal[0]), float(normal[1]), float(normal[2]))
        ok  &= obj.setNormal(i, 0, mxNormal)
        
    if not ok:
        raise("Error setting normals")
    
    # Triangles
    for i in range(nTriangles):
        triangle = triangles[i]
        v1 = int(triangle[0])
        v2 = int(triangle[1])
        v3 = int(triangle[2])
        n1 = int(triangle[3])
        n2 = n1
        n3 = n1
        assert(v1 < nVertices and v2 < nVertices and v3 < nVertices)
        assert(n1 < nNormals and n2 < nNormals and n3 < nNormals)
        
        if len(triangle) > 4:
            n2 = int(triangle[4])
            n3 = int(triangle[5])
            
        ok &= obj.setTriangle(i, v1, v2, v3, n1, n2, n3)
       
    if not ok:
        raise("Error setting triangles")
    
    return obj

'''
def toXML(obj, root):  
    
    # root element
    root = Element("scene")
    
    for key, value in obj.vars().items():
        SubElement(root, key).text = repr(value)
        
    return root

'''