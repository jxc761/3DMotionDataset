'''
Created on Feb 5, 2014

@author: Jing
'''
import pymaxwell as Mxs
import Configuration as Conf
import Utils
import numpy

class CPhotographer(object):
    '''
    classdocs
    '''
    
    # self, center, startPoint, axis, degree, sampleLv
    def __init__(self, conf):
        '''
        Constructor
        '''
        self.conf = conf
        self.fStop = conf.fStop
        self.focalLength = conf.focalLength
        self.time = conf.time
        self.fps  = conf.fps
        self.speed = conf.speed
        
    
    def Setup(self, focalPoint, initPosition, zAxis, motion_axis):
        self.initPosition =  initPosition
        self.focalPoint = focalPoint
        self.zAxis = zAxis
        self.motion_axis  = motion_axis

    # refer 2.4.7 Constructing a Basis from Two Vectors
    def getInitUp(self):
        va = self.target - self.initPosition
        vb = self.zAxis
        
        w = Utils.Normalize(va)
        u = Utils.Normalize(numpy.cross(w, vb))
        v = numpy.cross(w, u)
        
        return v
    


    def instantize(self, mxScene, name, frameIndex):
        '''
        return Maxwell camera  
        '''
        nSteps, shutter, filmWidth, filmHeight, iso, pDiaphragmType, angle, nBlades, \
                 fps, xRes, yRes, pixelAspect, projectType = self.GetFixParameters() 
        mxCamera = mxScene.addCamera(name, nSteps, shutter, filmWidth, filmHeight, iso, pDiaphragmType, angle, nBlades, 
                 fps, xRes, yRes, pixelAspect, projectType)

        focalPoint = self.focalPoint
        fStop = self.fStop 
        focalLength = self.focalLength  
        for iStep in range(self.nSteps):
            origin = self.GetPosition(frameIndex, iStep)
            up = self.GetUp(frameIndex, iStep)
            stepTime = self.GetStepTime(frameIndex, iStep)
            mxCamera.setStep(iStep, origin, focalPoint, up, focalLength, fStop, stepTime)
        
        return mxCamera
    
    def GetFixParameters(self):
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
        projectType     = self.conf.projectType
        
        return  (nSteps, shutter, filmWidth, filmHeight, iso, pDiaphragmType, angle, nBlades, 
                 fps, xRes, yRes, pixelAspect, projectType)
        
    def SetInitPosition(self, position):
        self.initPosition = position
        pass
    
    def GetInitPosition(self):
        return self.initPosition

    def SetFocalPoint(self, focalPoint):
        self.focalPoint = focalPoint
    
    def GetFocalPoint(self):
        return self.focalPoint
    
    def SetAxis(self, axis):
        self.axis = axis
    
    def GetAxis(self):
        return self.axis
 
    def GetFramesCount(self):
        return self.time / self.fps
    
    def GetFocalLength(self):
        return self.focalLength
     
    def SetFocalLength(self, focalLength):
        self.focalLength = focalLength
    
    # To be implemented    
    def GetPosition(self, iFrame, iStep):
        pass
 
    def GetUp(self, iFrame, iStep):
        pass
    
    def GetStepTime(self, iFrame, iStep):
        pass
  
    def GetTrajectory(self):  
        pass
    

    

class CRoateMovePhotographer(CPhotographer):
    
    initPosition = numpy.array([0, 0, 1])
    initUp = numpy.array([0, 0, 1])
    moveDirection = numpy.array[0, 0, 1]
   
    def GetPosition(self, iFrame, iStep):
        mtx = self.getTranformMtx(iFrame, iStep)
        return Utils.CTransform.transform(mtx, self.initPosition)
        
    def GetUp(self, iFrame, iStep):
        mtx = self.getTransformMtx(iFrame, iStep)
        initUp = self.getInitUp()
        return Utils.CTransform.transform(mtx, self.initUp)
    
    def GetStepTime(self, iFrame, iStep):
        return self.fps * iFrame +
  
    def GetTrajectory(self):  
        pass
    
    def getTranformMtx(self, iFrame, iStep):
        pass
        
    
'''
 
        time = iFrame * 1.0 / (self.fps*1.0)
      
        #TODO: error
        radian =self.speed * time
        
        center = self.focalPoint
        normal = self.axis   
        mtx = Utils.CTransform.Rotate(center, normal, radian)
        oldP = numpy.array([0, 0, 0, 1.0], numpy.double)
        oldP[0:2] = self.initPosition
        position = numpy.dot(oldP, mtx.transpose())
'''
    