'''
Created on Mar 4, 2014

@author: Jing
'''
import numpy
from src.vx.utils import utils as Utils
from src.vx.utils import transform as Transform


class CCameraOperatorParameter:
    def __init__(self, params):
        self.time = params.time
        self.speed = params.speed
        self.zAxis = params.zAxis
        self.fps = params.fps
        self.nStep = params.nStep
        self.fieldOfView = params.fieldOfView
        self.fieldOf
        pass
    
class CCameraOperator(object):
    '''
    classdocs
    '''
    
    def __init__(self, params):
        '''
        Constructor
        '''
        self.mvParams = params
        
    def setup(self, focalPoint, initPosition):
        self.focalPoint = focalPoint
        self.initPosition = initPosition
        
    def setMvParams(self, params):
        self.mvParmas = params
        
    ####################
    def setInitPosition(self, position):
        self.initPosition = position
    
    def getInitPosition(self):
        return self.initPosition

    def setFocalPoint(self, focalPoint):
        self.focalPoint = focalPoint
    
    def getFocalPoint(self):
        return self.focalPoint
    
    def setZAxis(self, axis):
        self.params.zAxis = axis
    
    def getZAxis(self):
        return self.params.zAxis
     
  
    # refer 2.4.7 Constructing a Basis from Two Vectors
    def getInitCameraUp(self):
        #va = self.getFocalPoint() - self.getInitPosition()
        va = self.getInitPosition() - self.getFocalPoint() # w
        vb = self.getZAxis() # up
        
        w = Utils.normalize(va) # w 
        u = Utils.normalize(numpy.cross(vb, w))
        v = numpy.cross(w, u)
        
        return v
    
    ####
    '''
    before call any function in following, you must have call
        setup()
    '''
        
    def getPosition(self, iFrame, iStep=0):
        mtx = self.getTransform(iFrame, iStep)
        pt = self.getInitPosition()
        return Transform.transform(mtx, pt)
       
    def getUp(self, iFrame, iStep=0):
        mtx = self.getTransform(iFrame, iStep)
        up = self.getInitCameraUp()
        o = numpy.array([0, 0, 0], dtype = numpy.double)
        newUp =  Transform.transform(mtx, up) - Transform.transform(mtx, o)
        return newUp
    
    def getStepTime(self, iFrame, iStep=0):
        # step per second
        return iStep / (self.fps * self.nSteps)
        
    def getFocalLength(self, iFrame=0, iStep=0):
        print(self.fieldOfView)
        focalLength = self.filmWidth / ( 2 * numpy.tan(self.fieldOfView/2) )

        return focalLength
    
    def getFramesCount(self): 
        return int(numpy.ceil(self.fps * self.time))
    
    
    def getTrajectory(self):  
        trajectory = []
        iStep = 0
        for iFrame in range(self.getFramesCount()):
            trajectory.append(self.getPosition(iFrame, iStep))
            
        return trajectory
    

    # To be implemented   
    def getTransform(self, iFrame, iStep):
        raise ("This is an interface.... error")
        pass 
    
    
    
class CRotateCamera(CCamera):
    def __init__(self, conf, zAxis, params = None):
        if params == None:
            params = zAxis
        super(CRotateCamera, self).__init__(conf, zAxis, params)
        
         
    def getRotateAxis(self):
        return self.mvParams
    
    def getTransform(self, iFrame, iStep):
        ###TODO
        time = iFrame * 1.0 / self.fps  + self.getStepTime(iFrame, iStep)
        radian = time * self.speed
        return Transform.rotate(self.focalPoint, self.getRotateAxis(), radian)
        
        