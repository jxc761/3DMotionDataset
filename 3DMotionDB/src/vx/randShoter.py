'''
Created on Feb 20, 2014

@author: Jing
'''

from shoter import CShoter
from src.vx.utils import utils
import math
import copy
class CRandShotScripts:
    
        def __init__(self, targets, eyes, directions, camera):
            self.eyes = eyes
            self.targets = targets
            self.directions = directions
            self.camera = camera
            print(eyes)
            print(targets)
            print(directions)
          
        def getId(self, idx):
            
            N = len(self.eyes)
            M = len(self.targets)
            D = len(self.directions)
           
            # idx = dId * (N * M) + eyeId * M + targetId
            directionId = int(math.floor(idx / (N*M) ))
            eyeId = int( math.floor( (idx - directionId * N * M) / M ) )
            targetId = int(idx - directionId * N * M - eyeId * M )
            assert (idx == directionId * (N * M) + eyeId * M + targetId)
            return (eyeId, targetId, directionId)
        
        def getIdxStr(self, idx):
            eyeId, targetId, directionId = self.getId(idx)
            idxStr = "e{}_t{}_d{}".format(eyeId, targetId, directionId)
            return idxStr
    
        def get(self, idx):
            eyeId, targetId, directionId = self.getId(idx)
            print((eyeId, targetId, directionId))
            self.camera.setup(self.targets[targetId], self.eyes[eyeId])
            self.camera.setMvParams(self.directions[directionId])    
            return self.camera
        
        def count(self):
            N = len(self.eyes)
            M = len(self.targets)
            D = len(self.directions)
            return N * M * D
        
class CRandShoter(CShoter):
    '''
    classdocs
    '''
         
    def __init__(self, conf, sceneControler, camera):
        '''
        Constructor
        '''
        self.sceneControler     = sceneControler
        self.camera             = camera
        self.conf               = conf
        
        self.numbOfDirections   = conf.numbOfViews
        self.numbOfTargets      = conf.numbOfTargets
        self.numbOfCameras      = conf.numbOfCameras
        self.minFocalDistance   = conf.minFocalDistance
        
        self.zAxis = sceneControler.getZAxis()
        
    def genShotScripts(self):
        
        # camera positions
        # focal points positions
        # rotate each camera around each position
        directions = []
        directions.append(self.zAxis)
        while len(directions) < self.numbOfDirections:
            directions.append(self.sceneControler.randDirection())
        
        
        numbOfTargets  = self.numbOfTargets
        targets = []
        while len(targets) < numbOfTargets :
            target = self.sceneControler.randPickPointOnFace()
            targets.append(target)
              
            
        numbOfCameras = self.numbOfCameras
        eyes = []
        while len(eyes) < numbOfCameras:
            eye = self.sceneControler.randPickPoint()
            if self.isLegalShot(eye, targets, directions):
                eyes.append(eye)
           
        scripts = CRandShoter.CRandShotScripts(targets, eyes, directions, self.camera)   
        return scripts
        
       
    def isLegalShot(self, eye, targets, directions):
        
        print("check if it is a legal shot.....")
        return True
        
        minFocalDistance = self.minFocalDistance
        
        tempCamera = copy.copy(self.camera)
        for target in targets:
            for direction in directions:
                tempCamera.setup(target, eye)
                tempCamera.setMvParams(direction)
                cameraTrajectory = tempCamera.getTrajectory()
                for pt in cameraTrajectory:
                    if utils.distance(target, pt) < minFocalDistance:
                        print("Utils.distance(focalPoint, pt) < minFocalDistance")
                        return False
                    if not self.sceneControler.isLegalCameraPosition(pt):
                        print("self.sceneControler.isLegalCameraPosition(pt)")
                        return False
                    if self.sceneControler.isOccluded(target, pt):
                        print("self.sceneControler.isOccluded(focalPoint, pt):")
                        return False

        return True
            
            
        
       
        