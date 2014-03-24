'''
Created on Feb 9, 2014

@author: Jing
'''
import random
import numpy
#import math

#import utils.transform as Transform
import utils.mxs as MXS
import utils.utils as Utils
import configuration as Configuration

class CSceneControler(object):
    '''
    classdocs
    '''

    '''
    TODO
    '''
    FloatInf = float('inf')
    FloatEps = 1e-5
    
    def __init__(self, mxScene, conf):
        '''
        Constructor
        '''
        self.scene = mxScene
        self.conf = conf
        self.pointsList, self.facesList, self.namesList = MXS.getObjectGeometris(mxScene)
    
    def getObjectsCount(self):
        return  len(self.namesList) 
    
    def getObjectFacesCount(self, objId):
        return self.facesList[objId].shape[0]
    
    def getObjectVerticesCount(self, objId):
        return self.pointsList[objId].shape[0]
    
    def getFaceVertices(self, objId, faceId):
        faces = self.facesList[objId]
        points = self.pointsList[objId]
        
        face = faces[faceId]
        pt1 = points[face[0]]
        pt2 = points[face[1]]
        pt3 = points[face[2]]
        
        return (pt1, pt2, pt3)

    ##### to be overriden 
    # test can we put a camera at the point
    def isLegalCameraPosition(self, point): 
        raise("This is an interface")
        pass
    
    def randPickPoint(self):
        raise("This is an interface")
        pass
    
    def getZAxis(self):
        raise("This is an interface")
        pass
    
    # test is there any object between pt1 and pt2
    def isOccluded(self, pt1, pt2):
        vd = pt2 - pt1
        tMax = Utils.norm2(vd)
        vd = Utils.normalize(vd)
        isIntersect, t = Utils.rayIntersectObjects(pt1, vd, self.facesList, self.pointsList, 0, tMax)
        
        return isIntersect
    
    def randPickPointOnFace(self):
        objId = random.randint(0, self.getObjectsCount()-1) #Return a random integer N such that a <= N <= b.
        faceId = random.randint(0, self.getObjectFacesCount(objId)-1)
        
        pt1, pt2 ,pt3 = self.getFaceVertices(objId, faceId)
        c1 = random.random()
        c2 = random.random()
        c3 = random.random()
        c = c1 + c2 + c3
        
        pt = (c1/c) * pt1 + (c2/c) * pt2 + (c3/c) * pt3
        return pt

  
    def randDirection(self):
        x = random.random()
        y = random.random()
        z = random.random()
        v = numpy.array([x, y, z], dtype=numpy.float32)
        v = Utils.normalize(v)
        return v
    
    def firstHit(self, pt, vd):
        tMin = 0
        tMax =  float('inf')
        isHit, t = Utils.rayIntersectObjects(pt, vd, self.facesList, self.pointsList, tMin, tMax)
        return (isHit, t)

class CBBoxSceneControler(CSceneControler):

        
    def __init__(self, mxScene, conf):
        # bbox 
        self.bbox, self.bboxPoints, self.bboxFaces, \
            self.bboxOrigin, self.bboxUAxis, self.bboxVAxis, self.bboxWAxis, \
            self.bboxDepth, self.bboxWidth, self.bboxHeight = self.readBBox(mxScene)
        
        super(CBBoxSceneControler, self).__init__(mxScene, conf)
    
    ###########################################
    # implement the methods
    def randPickPoint(self):
        u = random.random() * self.bboxDepth
        v = random.random() * self.bboxWidth
        w = random.random() * self.bboxHeight
        
        p = self.getWorldCoord(u, v, w)
        p = numpy.array(p, dtype=numpy.float32)
        return p
    
    def isLegalCameraPosition(self, point): 
        u, v, w = self.tranform2box(point)
        pt2 = self.getWorldCoord(u, v, 0)
        
        return not self.isOccluded(point, pt2)
    
    def getZAxis(self):
        
        return -1 * self.bboxWAxis
    
    '''
    def randDirection(self):
        
        print("random direction")
        d = self.getWorldCoord(1, 1, 1)
        print(repr(d))
        v = numpy.array(d, dtype=numpy.float32)
        print(repr(v))
        
        v = Utils.normalize(v)
        return v 

    def randPickPointOnFace(self):
        # objId = random.randint(0, self.getObjectsCount()-1) #Return a random integer N such that a <= N <= b.
        objId = self.namesList.index("coffee_table_top")
        print("the id of coffee_table_top is " + str(objId))
        faceId = random.randint(0, self.getObjectFacesCount(objId)-1)
        
        pt1, pt2 ,pt3 = self.getFaceVertices(objId, faceId)
        c1 = random.random()
        c2 = random.random()
        c3 = random.random()
        c = c1 + c2 + c3
        
        pt = (c1/c) * pt1 + (c2/c) * pt2 + (c3/c) * pt3
        return pt
    '''
  
    #############
    def getFixBBoxParams(self):
        bboxName        = Configuration.CBBoxConfig.BBoxName # "min_box_3dMotionDBSpecial"
        topMatName      = Configuration.CBBoxConfig.BBoxTopMaterial.upper()
        leftMatName     = Configuration.CBBoxConfig.BBoxLeftMaterial.upper()
        frontMatName    = Configuration.CBBoxConfig.BBoxFrontMaterial.upper()
        
        return (bboxName, topMatName, leftMatName, frontMatName)
    
    def readBBox(self, scene):
        '''
        ReadBBox(self, scene): -> bbox, origin, vu, vv, vw, depth, width, height
        '''
        (bboxName, topMatName, leftMatName, frontMatName) = self.getFixBBoxParams()
        
        # read the bbox from scene
        bbox = MXS.getObject(scene, bboxName)
        if bbox.isNull():
            raise ("cannot find the object named {}".format(bboxName))
        
        # hide the bbox
        MXS.setObjectInvisible(bbox)
     
   
        # read the top, left and right planes
        topTriIds = MXS.getObjectTrianglesByMat(bbox, topMatName)
        leftTriIds = MXS.getObjectTrianglesByMat(bbox, leftMatName)
        frontTriIds = MXS.getObjectTrianglesByMat(bbox, frontMatName)
 

        if len(topTriIds) ==0 or len(leftTriIds) == 0 or len(frontTriIds) == 0:
            raise ("cannot correct find min_box")
        
        # read the bbox geometry information
        points      = MXS.getObjectVertices(bbox)
        triangles   = MXS.getObjectTriangles(bbox)
        
        # make points set of three planes
        topPtsSet = set()
        for topTriId in topTriIds:
            vs = triangles[topTriId]
            topPtsSet.add(vs[0])
            topPtsSet.add(vs[1])
            topPtsSet.add(vs[2])
        
        leftPtsSet = set()
        for leftTriId in leftTriIds:
            vs = triangles[leftTriId]
            leftPtsSet.add(vs[0])
            leftPtsSet.add(vs[1])
            leftPtsSet.add(vs[2])
        
        frontPtsSet = set()
        for frontTriId in frontTriIds:
            vs = triangles[frontTriId]
            frontPtsSet.add(vs[0])
            frontPtsSet.add(vs[1])
            frontPtsSet.add(vs[2])
            
        # find origin, u, v, w
        oPtId = topPtsSet & leftPtsSet & frontPtsSet
        uPtId = (topPtsSet & leftPtsSet ) - oPtId
        vPtId = (topPtsSet & frontPtsSet) - oPtId
        wPtId = (leftPtsSet& frontPtsSet) - oPtId
        
        oPtId = oPtId.pop()
        uPtId = uPtId.pop()
        vPtId = vPtId.pop()
        wPtId = wPtId.pop()
        
        # normalize the vector
        origin = points[oPtId]
        vu = points[uPtId] - origin
        vv = points[vPtId] - origin
        vw = points[wPtId] - origin
        
        depth = Utils.norm2(vu)
        width = Utils.norm2(vv)
        height = Utils.norm2(vw)
        
        vu = Utils.normalize(vu)
        vv = Utils.normalize(vv) 
        vw = Utils.normalize(vw)
        print("box depth: "+str(depth))
        print("box width: "+str(width))
        print("box height: "+str(height))
        return (bbox, points, triangles, origin, vu, vv, vw, depth, width, height)

    def tranform2box(self, point):
        
        pt = point - self.bboxOrigin
        
        vu = self.bboxUAxis
        vv = self.bboxVAxis
        vw = self.bboxWAxis
            
        u = pt[0] * vu[0] + pt[1] * vu[1] + pt[2] * vu[2] # dot(pt, u)
        v = pt[0] * vv[0] + pt[1] * vv[1] + pt[2] * vv[2]
        w = pt[0] * vw[0] + pt[1] * vw[1] + pt[2] * vw[2]
        
        return (u, v, w)
    
    def getWorldCoord(self, u, v, w):
        pe = self.bboxOrigin
        vu = self.bboxUAxis
        vv = self.bboxVAxis
        vw = self.bboxWAxis
        
        x = pe[0] + u * vu[0] + v * vv[0] + w * vw[0]
        y = pe[1] + u * vu[1] + v * vv[1] + w * vw[1]
        z = pe[2] + u * vu[2] + v * vv[2] + w * vw[2]
        
        return  (x, y, z)
    