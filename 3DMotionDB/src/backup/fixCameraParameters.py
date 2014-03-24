'''
Created on Mar 3, 2014

@author: Jing
'''

class CFixCameraParameters(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        nSteps           = 1            # Number of steps.
         shutter          = 125          # Camera shutter (1/s).
         filmWidth        = 36           # Camera film width (mm).
         filmHeight       = 24           # Camera film height (mm).
         iso              = 100          # Camera ISO.

        pDiaphragmType   = "CIRCULAR"   # Diaphragm type. Possible values: "CIRCULAR" and "POLYGONAL".
        angle            = 0            # Shutter angle.
        nBlades          = 0            # Number of diaphragm blades if pDiaphragmType is "POLYGONAL".
    
        fps              = 1           # Frames per second.
        xRes             = 96           # Resolution output width.
        yRes             = 64           # Resolution output height.
        pixelAspect      = 1.0          # Pixel aspect ratio.
        projectionType   = 0            # Camera projection type. 0 (perspective, default), 
                                    # 1 (front), 2 (top), 3 (left), 4 (back), 5 (bottom), 6 (right).   
        focalLengthNeedCorrection=True  # Indicates whether focal length needs correction. Default value: 1 (true).
    
    #fStop            = 8            # 8, 11, 16 humman vision / 2.8 dark, 5.6 / 8 day light 
    #focalLength      = 35           # 35mm -> 50mm normal, 200/focal
    #fieldView        = 30           # degree
    fStop            = 5.6          
    fieldOfView      = 3.14 / 3     # radius
        
        self.nSteps          = conf.nSteps
        self.shutter         = conf.shutter
        self.filmWidth       = self.conf.filmWidth
        self.filmHeight      = self.conf.filmHeight
        self.iso             = self.conf.iso
        self.pDiaphragmType  = self.conf.pDiaphragmType
        angle           = self.conf.angle
        nBlades         = self.conf.nBlades
        fps             = self.conf.fps
        xRes            = self.conf.xRes
        yRes            = self.conf.yRes
        pixelAspect     = self.conf.pixelAspect
        projectType     = self.conf.projectionType
        
        return  (nSteps, shutter, filmWidth, filmHeight, iso, pDiaphragmType, angle, nBlades, 
                 fps, xRes, yRes, pixelAspect, projectType)