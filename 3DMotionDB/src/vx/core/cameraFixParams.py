'''
Created on Feb 19, 2014

@author: Jing
'''
class CCameraFixParams(object):
    '''
    classdocs
    '''
    
    def __getattr__(self):
        attrs =  ['nSteps', 'shutter', 'filmWidth', 'filmHeight', 'iso',
                 'pDiaphragmType', 'angle', 'nBlades', 
                 'fps', 'xRes', 'yRes', 'pixelAspect', 'projectionType', 
                 'focalLengthNeedCorrection', 
                 'fStop', 'fieldOfView' ]
    
        return attrs
    
    def initFixParams(self):
        self.nSteps           = 1            # Number of steps.
        self.shutter          = 125          # Camera shutter (1/s).
        self.filmWidth        = 36           # Camera film width (mm).
        self.filmHeight       = 24           # Camera film height (mm).
        self.iso              = 100          # Camera ISO.
    
        self.pDiaphragmType   = "CIRCULAR"   # Diaphragm type. Possible values: "CIRCULAR" and "POLYGONAL".
        self.angle            = 0            # Shutter angle.
        self.nBlades          = 0            # Number of diaphragm blades if pDiaphragmType is "POLYGONAL".
        
        self.fps              = 1           # Frames per second.
        self.xRes             = 96           # Resolution output width.
        self.yRes             = 64           # Resolution output height.
        self.pixelAspect      = 1.0          # Pixel aspect ratio.
        self.projectionType   = 0            # Camera projection type. 0 (perspective, default), 
                                        # 1 (front), 2 (top), 3 (left), 4 (back), 5 (bottom), 6 (right).   
        self.focalLengthNeedCorrection=True  # Indicates whether focal length needs correction. Default value: 1 (true).
        self.fStop            = 5.6          # 8, 11, 16 humman vision / 2.8 dark, 5.6 / 8 day light 
        self.fieldOfView      = 3.14 / 3     # radius
    
    def getStaticParams(self):
        return (self.nSteps, self.shutter, self.filmWidth, self.filmHeight, self.iso, self.pDiaphragmType, self.angle, self.nBlades, 
                 self.fps, self.xRes, self.yRes, self.pixelAspect, self.projectType)