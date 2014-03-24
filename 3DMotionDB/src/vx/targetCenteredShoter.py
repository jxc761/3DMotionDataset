'''
Created on Mar 3, 2014

@author: Jing
'''
import copy
import math
import random

import src.vx.utils.utils as Utils
from shoter import CShoter, CShotScripts

class CTargetCenteredShoter(CShoter):
    
    class CTargetCenteredShotScripts(CShotScripts):
        def __init__(self, focalPoints, camerasPositions, camera):
            self.cameras = camerasPositions
            self.focalPoints = focalPoints
            self.camera = camera
            
            self.nFocalPoints   = len(focalPoints)
            self.nDirections    = len(camerasPositions[0])
            self.nDistances     = len(camerasPositions[0][0])
            
        def count(self):
            return   self.nFocalPoints * self.nDirections  * self.nDistances
        
        def getIdx(self, idx):
            focalId = int(math.floor(idx / (self.nDirections * self.nDistances) ))
            directionId =int(math.floor(  (idx - focalId *  self.nDirections * self.nDistances) /  self.nDistances ) )   
            distanceId = int(idx - focalId *  self.nDirections * self.nDistances - directionId *  self.nDistances  )
            return (focalId,  directionId, distanceId)
            
        def getIdxStr(self, idx):
            focalId,  directionId, distanceId = self.getIdx(idx)
            return "f{}_v{}_p{}".format(focalId, directionId, distanceId)
        
        def get(self, idx):
            focalId,  directionId, distanceId = self.getIdx(idx)
            focalPoint= self.focalPoints[focalId]
            cameraPosition = self.cameras[focalId][directionId][distanceId]
            self.camera.setup(focalPoint, cameraPosition)
            return self.camera
    """
    """
    
    def __init__(self, conf, sceneControler, cinematographer):
        
        self.minFocalDistance   = conf.minFocalDistance #
        self.numbOfTargets      = conf.numbOfTargets    # the number of targets will be choose
        self.numbOfViews        = conf.numbOfViews      # for each target, we will shot in "numbOfViews" directions
        self.numbOfCameras      = conf.numbOfCameras    # the number of different view points in each direction
        self.sceneControler     = sceneControler        # the scene controler which can pick focal points and put camera into the scene
        self.cinematographer    = cinematographer       # the cinematographer that can control the movement of a camera
        
        self.maxIt  =  1000
        
        self.normalVector = sceneControler.getZAxis()

        
    def genShotScripts(self):
        # focalPoints[i] refers to the coordinate of a focal point 
        focalPoints = []       
        
        # cameraPositions works like a three dimensional array.
        # cameraPositions[i] refers to a list of camera positions around focalPoints[i]
        # cameraPositions[i][j] refers to a list of camera positions around focalPoints[i] in the same direction
        # cameraPositions[i][j][k] refers to the k-th camera position around focalPoint[i] in the direction[j]
        cameraPositions = []    
        for targetId in range(self.numbOfTargets):
            print("try to shot the {}-th focal point.....".format(targetId))
            focalPoint, positions = self.randShot()
            focalPoints.append(focalPoint) 
            cameraPositions.append(positions)
            print("finish shot the {}-th focal point....".format(targetId))
        
        scripts = self.CTargetCenteredShotScripts(focalPoints, cameraPositions, self.cinematographer)
        print("finish generate shooting script")
        return scripts
    
    #############################################################################
    # In the future, following methods will become private, so don't call them.
    #############################################################################
    def randShot(self):
        """
        Method: randShoot()->(focalPoint, cameraPositions) 
        This method is 
        """
        maxIt = self.maxIt
        
        for it in range(maxIt):
            focalPoint = self.sceneControler.randPickPointOnFace() # candidate focal points
            ok, cameraPositions = self.shotAroundTarget(focalPoint)
            if ok:
                return (focalPoint, cameraPositions)
            
        raise "It has reached the max iteration number and we cannot pick out a good focal point. You can try again."
    
    def shotAroundTarget(self, target):
       
        maxIt = 10
        numbOfViews = self.numbOfViews
        
        print("try to shot current selected target in {} directions".format(numbOfViews))
        cameraPositions = []
        for it in range(maxIt):
            vd = self.sceneControler.randDirection()
            ok, positions = self.shotInDirection(target, vd)
            if ok:
                cameraPositions.append(positions)
                
            if len(cameraPositions) >= numbOfViews:
                print("finish shot around the target in {} directions".format(numbOfViews))
                return (True, cameraPositions)
        
        print("failed to shot around the target")
        return (False, False)
    
    def shotInDirection(self, target, vDirection):
        print("try to shot a target in a direction")
        maxIt = 10
        numb = self.numbOfCameras
        positions = []
        tMin = self.minFocalDistance
        
        for it in range(maxIt):    
            # randomly select a position in the direction
            isHit, tMax = self.sceneControler.firstHit(target, vDirection)
            if not isHit or tMax < tMin:
                print(isHit)
                print(tMax)
                print("It is not legal shot direction for the target")
                return (False, False)
            
            ## todo 
            t = random.random() * (tMax-tMin) + tMin
            pos = target + t * vDirection 
            
            # check if we can successfully observe the target from the position
            if self.isLegalShot(target, pos):
                positions.append(pos)
                if len(positions) >= numb:
                    print("finish shooting a target in a direction")
                    return (True, positions)
        
        print("fail to shot a target in a direction")
        return (False, False)
    

    def isLegalShot(self, focalPoint, position):
        
        print("testing if the current setup is feasible")
        minFocalDistance = self.minFocalDistance
        
        tempCamera = copy.copy(self.cinematographer)
        tempCamera.setup(focalPoint, position)
        
        trajectory = tempCamera.getTrajectory()
        ok, msg = self.isFeasible(focalPoint, trajectory, minFocalDistance, self.sceneControler)
        print msg
        return ok
    
    
    def isFeasible(self, focalPoint, trajectory, minFocalDistance, scene):
        
        for idx in range(1, len(trajectory), 32):
            print(idx)
            pt = trajectory[idx]
            if Utils.distance(focalPoint, pt) < minFocalDistance:
                msg = "A position in the camera trajectory is too close to the target!"
                return (False, msg)
            if not scene.isLegalCameraPosition(pt):
                msg = "A position in the camera trajectory is not a good place to put camera!"
                return (False, msg)
            if scene.isOccluded(focalPoint, pt):
                msg = "A position in the camera trajectory cannot see the target"
                return (False, msg)
            
        msg = "A Legal Shot"
        return (True, msg)
