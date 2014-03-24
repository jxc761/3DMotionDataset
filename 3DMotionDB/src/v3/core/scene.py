'''
Created on Mar 4, 2014

@author: Jing
'''
from src.vx.utils import mxs as MXS
from src.vx.utils import geom as Geom
from src.vx.utils import utils as Utils

class CScene(object):
    '''
    classdocs
    '''
    def __init__(self, mxScene):
        '''
        Constructor
        '''
        self.pointsList, self.facesList, self.namesList = MXS.getObjectGeometris(mxScene)
        self.bboxsList = self.__computeBBox()

    def firstHit(self, pt, vd):
        tMin = 0
        tMax = float('inf')
        
        isHit, t = self.__intersect(pt, vd, tMin, tMax)
        return (isHit, t)
       
    def isOccluded(self, pt1, pt2):
        """To check if there is a object between pt1 and pt2
        
        Methods: isOccluded(pt1, pt2) -> isOccluded?
        """
        vd = pt2 - pt1
        tMax = Utils.norm2(vd)
        vd = Utils.normalize(vd)
        isIntersect, t = self.__intersect(pt1, vd, 0, tMax)
        return isIntersect
    
    
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
    
    def __computeBBox(self):
        bboxsList = []
        for points in self.pointsList:
            bbox = self.__getObjBBox(points)    
        return bboxsList
    
    def __getObjBBox(self, points):
        
        maxx=points[0][0]
        maxy=points[0][1]
        maxz=points[0][2]
        minx=maxx
        miny=maxy
        minz=maxz
        
        for pt in points:
            if pt[0] > maxx:
                maxx=pt[0]
            
            if pt[1] > maxy:
                maxy=pt[1]
            
            if pt[2] > maxz:
                maxz=pt[2]        
            
            if pt[0] < minx:
                minx=pt[0]
                
            if pt[1] < miny:
                miny=pt[1]
                
            if pt[2] < minz:
                minz=pt[2]
        
        
        origin = [minx, miny, minz]
        u = [maxx-minx, 0, 0]
        v = [0, maxy-miny, 0]
        w = [0, 0, maxz-minz]
        box = Geom.CBox(origin, u, v, w)
        return box
    
    def __intersect(self, pt, vd, tMin, tMax):
        isHit = False
        hitT = False
        
        hits = self.__HittingBBoxs(pt, vd)
        for hitId in range(hits):
            faces = self.facesList[hitId]
            points = self.pointsList[hitId]
            isIntersect, t = Utils.rayIntersectObject(pt, vd, faces, points, tMin, tMax)
            if isIntersect:
                isHit = True
                tMax = t
                hitT = t
        
        return (isHit, hitT)
    
    def __HittingBBoxs(self, pt, vd):
        
        tMin = 0
        tMax = float('inf')
        hits = []

        for bboxId in range(self.getObjectsCount()):
            bbox = self.bboxsList[bboxId]
            faces=bbox.getTriangles()
            points=bbox.getVertices()
            isIntersect, t = Utils.rayIntersectObject(pt, vd, faces, points, tMin, tMax)
            if isIntersect:
                hits.append(bboxId)
                
        return hits 
