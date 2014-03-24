'''
Created on Feb 2, 2014

@author: Jing
'''
from pymaxwell import *
import numpy
import math
import random

import xml.etree.ElementTree as xmlElementTree
from xml.etree.ElementTree import Element, SubElement, ElementTree, dump, tostring
import xml.dom.minidom as MiniDom

class ObjectType:        
    Group, Instance, Geometry, Unkown=range(4)


def GetObjectType(obj):
    
    objType = ObjectType.Group
    isMeshed, ok = obj.isMesh()
    if isMeshed == 0: # this object is not meshed
        isInstance, ok = obj.isInstance()
        if isInstance == 1:
            objType = ObjectType.Instance
        else:
            objType = ObjectType.Unkown
    else: # this object is meshed
        nTriangles, ok = obj.getTrianglesCount()
        if nTriangles > 0:
            return ObjectType.Geometry
        else:
            return ObjectType.Unkown
        
    return objType


def GetObjectVertices(obj, step=0):
    '''
    return  the world/global coordinates of all vertices
    '''
    
    objType = GetObjectType(obj)
    assert objType == ObjectType.Instance or objType== ObjectType.Geometry
    
    # get the transformation matrix 
    base, ok = obj.getWorldTransform()
    u = (base.xAxis[0], base.xAxis[1], base.xAxis[2])
    v = (base.yAxis[0], base.yAxis[1], base.yAxis[2])
    w = (base.zAxis[0], base.zAxis[1], base.zAxis[2])
    o = (base.origin[0], base.origin[1], base.origin[2])
    transfMtx = numpy.array([u, v, w, o], dtype=numpy.float32)
    
    # get the coordinates of all vertices
    realObj = obj
    if objType == ObjectType.Instance:
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

def GetObjectTriangles(obj):

    objType = GetObjectType(obj)
    assert objType == ObjectType.Instance or objType== ObjectType.Geometry

    realObj = obj
    if objType == ObjectType.Instance:
        realObj = obj.getInstanced()
        
    nTriangles, ok = realObj.getTrianglesCount()
    faces = numpy.zeros((nTriangles, 3), dtype=numpy.uint32)
    for tId in range(nTriangles):
        triangle = realObj.getTriangle(tId)
        faces[tId][0] = triangle[0]
        faces[tId][1] = triangle[1]
        faces[tId][2] = triangle[2]
        
    return faces

def IsHitTriangle(pe, vd, pa, pb, pc, minT, maxT):
    '''
    Method: IsHitTriangle(pe, vd, pa, pb, pc, minT, maxT) -> (isHit, t)
    Description: check whether the line segment pe + t vd ( minT <= t <= maxT)hit the triangle <pa, pb, pc> 
    '''
    a = pa[0] - pb[0]
    b = pa[1] - pb[1]
    c = pa[2] - pb[2]
    
    d = pa[0] - pc[0]
    e = pa[1] - pc[1]
    f = pa[2] - pc[2]
    
    g = vd[0]
    h = vd[1]
    i = vd[2]
    
    j = pa[0] - pe[0]
    k = pa[1] - pe[1]
    l = pa[2] - pe[2]
    
    f1 = e * i - h * f
    f2 = g * f - d * i
    f3 = d * h - e * g
    
    f4 = a * k - j * b
    f5 = j * c - a * l
    f6 = b * l - k * c
    
    M = a * f1 + b * f2 + c * f3
    
    if M == 0 : # no solution
        return (False, 0)
    
    t = - (f* f4 + e * f5 + d * f6) / M
    
    if t < minT or t > maxT:
        return (False, t)
    
    gamma = (i * f4 + h * f5 + g * f6) / M
    if gamma < 0 or gamma > 1:
        return (False, t)
    
    beta = (j * f1 + k * f2 + l * f3) / M
    if beta < 0 or beta > 1:
        return (False, t)
    
    return (True, t)

def GetObjectGeometris(scene):
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
        
        if not IsSkip(curObj):
            points = GetObjectVertices(curObj)
            faces =  GetObjectTriangles(curObj)
            name =  curObj.getName()
            pointsList.append(points)
            facesList.append(faces)
            namesList.append(name)     
            
        curObj = it.next()
        
    return (pointsList, facesList, namesList)

def IsSkip(obj):
    
    objType = GetObjectType(obj)
    isNotGeom = not ( (objType == ObjectType.Instance) or  (objType == ObjectType.Geometry) )
    isHidden, ok = obj.getHide()
    isHideToCamera,ok = obj.getHideToCamera()
    
    return (isNotGeom or isHidden or isHideToCamera)



def Norm2(v):
    norm = 0
    for vi in v:
        norm += vi * vi
    return math.sqrt(norm)

def Normalize(v):
    norm = Norm2(v)
    for i in range(len(v)):
        v[i] = v[i] / norm    
    return v


class CTransform:
    
    def Transform(self, point, mtx):     
        pt = numpy.array([[point[0]], [point[1]], [point[2]], [1]],  numpy.double)
        newpt = numpy.dot(mtx, pt)
        return newpt.transpose()
    
        
    def RotateAroundXAxis(self, radian):
        cos_r = math.cos(radian)
        sin_r = math.cos(radian)
        
        mtx = numpy.array([[1,     0,      0,  0],
                           [0, cos_r, -sin_r, 0], 
                           [0, sin_r,  cos_r, 0], 
                           [0,     0,      0, 1]],dtype=numpy.double)
        return mtx
    
    def RotateAroundYAxis(self, radian):
        cos_r = math.cos(radian)
        sin_r = math.cos(radian)
        mtx = numpy.array([[ cos_r, 0, sin_r, 0],
                           [     0, 1,     0, 0], 
                           [-sin_r, 0, cos_r, 0], 
                           [     0, 0,     0, 1]],dtype=numpy.double)
        return mtx
    
    def RotateAroundZAxis(self, radian):
        cos_r = math.cos(radian)
        sin_r = math.cos(radian)
        mtx = numpy.array([[cos_r, -sin_r, 0, 0], 
                           [sin_r,  cos_r, 0, 0],
                           [    0,      0, 1, 0], 
                           [    0,      0, 0, 1]], dtype=numpy.double)
        return mtx
    
    
     
    def Rotate(self, center, normal, radian):
        '''
        Refer:
        http://inside.mines.edu/~gmurray/ArbitraryAxisRotation/
        '''
        normal = Normalize(normal)
        a = center[0]
        b = center[1]
        c = center[2]
        
        u = normal[0]
        v = normal[1]
        w = normal[2]
        u2 = u * u
        v2 = v * v
        w2 = w * w
        
        cost = math.cos(radian)
        sint = math.sin(radian)
        rcost = 1 - cost
        
        mtx = numpy.ones([4, 4], dtype=numpy.double)
        mtx[0][0] = u2 + (v2 + w2) * cost
        mtx[0][1] = u * v * rcost - w * sint
        mtx[0][2] = u * w * rcost + v * sint
        mtx[0][3] = (a * (v2 + w2)-u * (b*v + c*w)) * rcost + (b*w-c*v) * sint
        
        mtx[1][0] = u * v * rcost + w * sint
        mtx[1][1] = v2 + (u2 + w2) * cost
        mtx[1][2] = v * w * rcost - u * sint
        mtx[1][3] = (b * (u2 + w2) - v * (a*u+c*w) ) * rcost + (c*u-a*w) * sint
        
        mtx[2][0] = u * w * rcost - v * sint
        mtx[2][1] = v * w * rcost + u * sint
        mtx[2][2] = w2 + (u2 + v2) * cost
        mtx[2][3] = ( c * (u2+v2) - w * (a*u + b*v) ) * rcost + (a*v-b*u) * sint
        
        mtx[3][0] = 0
        mtx[3][1] = 0
        mtx[3][2] = 0
        mtx[3][3] = 1
        
        return mtx
    
    def transform(self, mtx, point):
        newPoint = [0.0, 0.0, 0.0]
        newPoint[0] =  mtx[0][0] * point[0] + mtx[0][1] * point[1] + mtx[0][2] * point[2] + mtx[0][3] 
        newPoint[1] =  mtx[1][0] * point[0] + mtx[1][1] * point[1] + mtx[1][2] * point[2] + mtx[1][3] 
        newPoint[2] =  mtx[2][0] * point[0] + mtx[2][1] * point[1] + mtx[2][2] * point[2] + mtx[2][3] 
        
        return newPoint
            
        
def RandSelectDirection(self):
    isZero = False 
    while isZero: 
        dx = random.random()
        dy = random.random()
        dz = random.random()
        norm = numpy.sqrt(dx * dx + dy * dy + dz * dz)
        isZero = norm < self.FloatEps
    
    vectd = numpy.array([dx/norm, dy/norm, dz/norm])
    return vectd
     
def RayIntersectObject(pt, vd, faces, points, tMin, tMax):
    for fId in range(faces.shape[1]):
        a = points[faces[fId][0]]
        b = points[faces[fId][1]]
        c = points[faces[fId][2]]
        isIntersect, t = IsHitTriangle(pt, vd, a, b, c, tMin, tMax)
        if isIntersect:
            tMax = t
    return (isIntersect, t)

  
def BuildObjectElement(elem, obj):
    
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
    
    

def SaveXML(root, pzFile):
    """
    Method: SaveXML(Element root, string pzFile)
    Description: format xml to a pretty-printed string and write it out
    """
    doc = MiniDom.parseString(xmlElementTree.tostring(root))
    prettyxml = doc.toprettyxml(indent="   ", newl="\r\n") #  encoding='utf-8'
    file_object = open(pzFile, "w")
    file_object.write(prettyxml)
    file_object.close()



def ExportMxsObjInformation(scene, pzFile):
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
        BuildObjectElement(objElem, curObj)
        objElemList.append(objElem)
        curObj = it.next()
    
    # write the document to a file
    # ElementTree(root).write(pzFile)
    SaveXML(root, pzFile) 
    print "finish export mxs information"


   
 