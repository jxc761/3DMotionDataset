'''
Created on Feb 5, 2014

@author: Jing
'''
import numpy
import random
import Utils
import Configuration as Conf
import Photographer
from pymaxwell import *

class CExperimenter:
    '''
    TODO
    '''
    FloatInf = float('inf')
    FloatEps = 1e-5

    def __init__(self, mxScene, conf):
        '''
        Constructor
        '''
        # points faces, and names
        self.pointsList, self.facesList, self.namesList = Utils.GetObjectGeometris(mxScene)
        self.scene = mxScene
        self.pzOutputDir = conf.pzOutputDir
        self.conf = conf
        self.camera = Photographer.CPhotographer()
    
    def SerializeObservation(self): 
        nFrames = self.camera.GetFramesCount()
        for iFrame in range(nFrames): 
            cameraName = self.GetCameraName(iFrame)
            camera = self.camera.instantize(self.scene, cameraName, iFrame)
            camera.setActive()
            pzOutMxs = self.GetSceneFilePath(iFrame)
            self.scene.writeMXS(pzOutMxs)
            
    def GetCameraName(self, iFrame):
        return "frame_{:05d}".format(iFrame)
    
    def GetSceneFilePath(self, iFrame):
        return "frame_{:05d}".format(iFrame)
    
    def SetUpCamera(self): 
        isLegal = False
        while not isLegal:
            target      = self.RandSelectFocalPoint()
            eye         = self.RandomPutCamera()
            
            self.camera.SetTarget(target)
            self.camera.SetInitPosition(eye)
            trajectory  = self.camera.GetTrajectory()
            isLegal = self.IsLegal(target,trajectory)
    
         
    # Primitive operations
    def RandomPutCamera(self):
        pass
    
    def IsLegal(self, target, cameraTrajectory):
        pass
        #return True 
    
    
    # default operations
    def RandSelectFocalPoint(self):
        objId = random.randint(0, self.GetObjectsCount()-1)
        faceId = random.randint(0, self.GetObjectFacesCount(objId)-1)
        
        pt1, pt2 ,pt3 = self.GetVertices(objId, faceId)
        c1 = numpy.random()
        c2 = numpy.random()
        c3 = numpy.random()
        c = c1 + c2 + c3
        
        pt = (c1/c) * pt1 + (c2/c) * pt2 + (c3/c) * pt3
        return pt
    
    # Simple geometry operation 
    def RayIntersectModel(self, pt, vd):
        tMin = 0
        tMax = self.FloatInf
        for objId in range(self.GetObjectCount()):
            faces = self.facesList[objId]
            points = self.pointsList[objId]
            isIntersect, t = Utils.RayIntersectObject(pt, vd, faces, points, tMin, tMax)
            if isIntersect:
                tMax = t
        return (isIntersect, t)
    
   
    def GetObjectsCount(self):
        return  len(self.namesList) 
    
    def GetObjectFacesCount(self, objId):
        return self.facesList[objId].shape[0]
    
    def GetObjectVerticesCount(self, objId):
        return self.pointsList[objId].shape[0]
    
    def GetVertices(self, objId, faceId):
        faces = self.facesList[objId]
        points = self.pointsList[objId]
        
        face = faces[faceId]
        pt1 = points[face[0]]
        pt2 = points[face[1]]
        pt3 = points[face[2]]
        
        return (pt1, pt2, pt3)

class CExperimenterForCubicInterior(CExperimenter):
    
    def __init__(self, mxScene, conf):
        # bbox 
        self.bbox, self.bboxPoints, self.bboxFaces, \
            self.bboxOrigin, self.bboxUAxis, self.bboxVAxis, self.bboxWAxis, \
            self.bboxDepth, self.bboxWidth, self.bboxHeight = self.ReadBBox(mxScene)
        
        super(CExperimenter, self).__init__(mxScene, conf)
            
   
    def IsLegal(self, target, trajectory): 

        for point in trajectory:
            vd = point - target
            T = Utils.Norm2(vd)
            vd = Utils.Normalize(vd)
            isIntersect, t = self.RayIntersectModel(target, vd)
            if isIntersect and t < T:
                return False
        
        return True
    
    def RandomPutCamera(self):
        u = random.random() * self.bboxDepth
        v = random.random() * self.bboxWidth
        w = random.random() * self.bboxHeight
        
        p = u * self.bboxUAxis + v * self.bboxVAxis + w * self.bboxWAxis
    
        return p
    
        
    def ReadBBox(self, scene):
        '''
        ReadBBox(self, scene): -> bbox, origin, vu, vv, vw, depth, width, height
        '''
        
        bboxName        = Conf.CBBoxConfig.BBoxName # "min_box_3dMotionDBSpecial"
        topMatName      = Conf.CBBoxConfig.BBoxTopMaterial.upper()
        leftMatName     = Conf.CBBoxConfig.BBoxLeftMaterial.upper()
        frontMatName    = Conf.CBBoxConfig.BBoxFrontMaterial.upper()
        
        # read the bbox from scene
        bbox = scene.getObject(bboxName)
        if bbox.isNull():
            raise ("cannot find the object named " + bboxName)
        
        # hide the bbox
        bbox.setHide(True)
        bbox.setHideToCamera(True)
        bbox.setHideToGI(True)
        bbox.setHideToReflectionsRefractions(True)
        
        # read the top, left and right planes
        nv = bbox.getTriangleCount()
        topTriIds = []
        leftTriIds = []
        frontTriIds = []
        for i in range(nv):
            mat, ok = CmaxwellObject.getTriangleMaterial(i)
            if ok:
                matName = mat.getName().upper()
                if matName == topMatName:
                    topTriIds.append(i)
                elif matName == leftMatName:
                    leftTriIds.append(i)
                elif matName == frontMatName:
                    frontTriIds.append(i)

        if len(topTriIds) ==0 or len(leftTriIds) == 0 or len(frontTriIds) == 0:
            raise ("cannot correct find min_box")
        
        # read the bbox geometry information
        points      = Utils.GetObjectVertices(bbox)
        triangles   = Utils.GetObjectTriangles(bbox)
        
        # make points set of three planes
        topPtsSet = {}
        for topTriId in topTriIds:
            vs = triangles[topTriId]
            topPtsSet.add(vs[0])
            topPtsSet.add(vs[1])
            topPtsSet.add(vs[2])
        
        leftPtsSet = {}
        for leftTriId in leftTriIds:
            vs = triangles[leftTriId]
            leftPtsSet.add(vs[0])
            leftPtsSet.add(vs[1])
            leftPtsSet.add(vs[2])
        
        frontPtsSet = {}
        for frontTriId in leftTriIds:
            vs = triangles[frontTriId]
            frontPtsSet.add(vs[0])
            frontPtsSet.add(vs[1])
            frontPtsSet.add(vs[2])
            
        # find origin
        oPtId = (topPtsSet & leftPtsSet & leftPtsSet).pop()
        uPtId = (topPtsSet & leftPtsSet ) - {oPtId}
        vPtId = (topPtsSet & frontPtsSet) -{oPtId}
        wPtId = (leftPtsSet& frontPtsSet) - {oPtId}
        
        # normalize the verctor
        origin = points[oPtId]
        vu = points[uPtId] - origin
        vv = points[vPtId] - origin
        vw = points[wPtId] - origin
        
        depth = numpy.inner(vu, vu) **.5
        width = numpy.inner(vv, vv) **.5
        height = numpy.inner(vw, vw)**.5
        
        vu = vw / depth
        vv= vv / width 
        vw = vu / height
        return (bbox, points, triangles, origin, vu, vv, vw, depth, width, height)
    '''
    def RayIntersectBBox(self, pt, vd):
        faces = self.bboxFaces
        points = self.bboxPoints
        tMin = 0
        tMax = self.FloatInf
        return Utils.RayIntersectObject(pt, vd, faces, points, tMin, tMax)
        
     def RandSelectDistance(self, pt, vd):
        (isIntersect, maxDistance) = self.RayIntersectHitBBox(pt, vd)
        if not isIntersect:
            raise "mxs does not meet our requirements!"
        return maxDistance * random.random()
    '''

            