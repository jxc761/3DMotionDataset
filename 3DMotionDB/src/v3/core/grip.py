import numpy
import random

from scene import CScene
from src.vx.utils import utils as Utils

class CKeyGripParams:
    def __init__(self, conf):
        self.sampleLevel = conf.sampleLevel
        self.safeDist = conf.minFocalDistance
        
    
class CKeyGrip:
    
    def __init__(self, mxScene, params):
        self.mxScene = mxScene
        self.scene = CScene(mxScene)
        self.pramas = params
    
    def getZAxis(self):
        raise("This is an interface")
        pass
    
    def randPickPoint(self):
        raise("This is an interface")
        pass
    
    def randPickPointOnFace(self):
        objId = random.randint(0, self.scene.getObjectsCount()-1) #Return a random integer N such that a <= N <= b.
        faceId = random.randint(0, self.scene.getObjectFacesCount(objId)-1)
        
        pt1, pt2 ,pt3 = self.scene.getFaceVertices(objId, faceId)
        c1 = random.random()
        c2 = random.random()
        c3 = random.random()
        c = c1 + c2 + c3
        
        pt = (c1/c) * pt1 + (c2/c) * pt2 + (c3/c) * pt3
        return pt
  
    def randPickDirection(self):
        x = random.random()
        y = random.random()
        z = random.random()
        v = numpy.array([x, y, z], dtype=numpy.float32)
        v = Utils.normalize(v)
        return v
    
    def isFeasibleCameraPosition(self, position): 
        raise("This is an interface")
        pass
    
    def isFeasible(self, focalPoint, cameraTrajectory):
        
        for i in range(0, len(cameraTrajectory), self.pramas.sampleLevel):
            position = cameraTrajectory[i]
            dist = Utils.distance(focalPoint, position)
            if dist < self.pramas.safeDist:
                msg = "too close"
                return (False, msg)
            if self.scene.isOccluded(focalPoint, position):
                msg = "occluded"
                return (False, msg)
            if not self.isFeasibleCameraPosition(position):
                msg = "infeasible camera position"
                return (False, msg)
            
        msg = "feasible"
        return (True, msg)
    