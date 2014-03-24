'''
Created on Feb 9, 2014

@author: Jing
'''
import utils.transform as Transform
import utils.utils as Utils
import utils.mxs as MXS
import numpy

class CCamera(object):
    '''
    classdocs
    '''

    def __init__(self, conf, zAxis, params):
        '''
        Constructor
        '''
        self.conf           = conf
        
        self.filmWidth      = conf.filmWidth
        self.fStop          = conf.fStop
        self.fieldOfView    = conf.fieldOfView
        self.fps            = conf.fps
        self.nSteps         = conf.nSteps
        
        self.time           = conf.time
        self.speed          = conf.speed
        
        self.zAxis          = zAxis
        self.mvParams       = params
        
    def setup(self, focalPoint, initPosition):
        '''
        '''
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
        self.zAxis = axis
    
    def getZAxis(self):
        return self.zAxis
     
    def getFieldOfView(self):
        return self.fieldOfView
    
    def setFieldOfView(self, fieldOfView):
        self.fieldOfView = fieldOfView
    
    ####
    def instantilize(self, mxScene, cameraName, frameIndex):
        '''
        return Maxwell camera  
        '''
        nSteps, shutter, filmWidth, filmHeight, iso, pDiaphragmType, angle, nBlades, \
                 fps, xRes, yRes, pixelAspect, projectType = self.getFixParameters() 
        mxCamera = mxScene.addCamera(cameraName, nSteps, shutter, filmWidth, filmHeight, iso, pDiaphragmType, angle, nBlades, 
                 fps, xRes, yRes, pixelAspect, projectType)
        
        #mxCamera.setHide(True) # not visible to other cameras

        focalPoint = self.focalPoint
        fStop = self.fStop 
        
        for iStep in range(self.nSteps):        
            origin = self.getPosition(frameIndex, iStep)
            up = self.getUp(frameIndex, iStep)
            stepTime = self.getStepTime(frameIndex, iStep)
            focalLength = self.getFocalLength(frameIndex, iStep)
            MXS.setStep(mxCamera, iStep, origin, focalPoint, up, focalLength, fStop, stepTime, 1)
        
        mxCamera.setActive()
        return mxCamera
    
    def getFixParameters(self):
        nSteps          = self.conf.nSteps
        shutter         = self.conf.shutter
        filmWidth       = self.conf.filmWidth
        filmHeight      = self.conf.filmHeight
        iso             = self.conf.iso
        pDiaphragmType  = self.conf.pDiaphragmType
        angle           = self.conf.angle
        nBlades         = self.conf.nBlades
        fps             = self.conf.fps
        xRes            = self.conf.xRes
        yRes            = self.conf.yRes
        pixelAspect     = self.conf.pixelAspect
        projectType     = self.conf.projectionType
        
        return  (nSteps, shutter, filmWidth, filmHeight, iso, pDiaphragmType, angle, nBlades, 
                 fps, xRes, yRes, pixelAspect, projectType)
        
    
    ####
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
    
        