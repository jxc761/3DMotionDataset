'''
Created on Mar 4, 2014

@author: Jing
'''
     
class CCameraParams(object):
    def __init__(self, conf):
        self.nSteps           = conf.nSteps             # Number of steps.
        self.shutter          = conf.shutter            # Camera shutter (1/s).
        self.filmWidth        = conf.filmWidth          # Camera film width (mm).
        self.filmHeight       = conf.filmHeight         # Camera film height (mm).
        self.iso              = conf.iso                # Camera ISO.
    
        self.pDiaphragmType   = conf.pDiaphragmType     # Diaphragm type. Possible values: "CIRCULAR" and "POLYGONAL".
        self.angle            = conf.angle              # Shutter angle.
        self.nBlades          = conf.nBlades            # Number of diaphragm blades if pDiaphragmType is "POLYGONAL".
        
        self.fps              = conf.fps                # Frames per second.
        self.xRes             = conf.xRes               # Resolution output width.
        self.yRes             = conf.yRes               # Resolution output height.
        self.pixelAspect      = conf.pixelAspect        # Pixel aspect ratio.
        self.projectionType   = conf.projectionType     # Camera projection type. 0 (perspective, default), 
                                                        # 1 (front), 2 (top), 3 (left), 4 (back), 5 (bottom), 6 (right).   
        self.focalLengthNeedCorrection=True             # Indicates whether focal length needs correction. Default value: 1 (true).
        self.fStop            = conf.fStop              # 8, 11, 16 humman vision / 2.8 dark, 5.6 / 8 day light 
        self.fieldOfView      = conf.fieldOfView        # radius

class CCinematographer(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.params=params
        
        
         
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
        nSteps          = self.params.nSteps
        shutter         = self.params.shutter
        filmWidth       = self.params.filmWidth
        filmHeight      = self.params.filmHeight
        iso             = self.params.iso
        pDiaphragmType  = self.params.pDiaphragmType
        angle           = self.params.angle
        nBlades         = self.params.nBlades
        fps             = self.params.fps
        xRes            = self.params.xRes
        yRes            = self.params.yRes
        pixelAspect     = self.params.pixelAspect
        projectType     = self.params.projectionType
        
        return  (nSteps, shutter, filmWidth, filmHeight, iso, pDiaphragmType, angle, nBlades, 
                 fps, xRes, yRes, pixelAspect, projectType)
        
    
    ####
        
        
        