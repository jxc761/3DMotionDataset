'''
Created on Feb 3, 2014

@author: Jing
'''

class CConfig:
    # path configuration
    pzConf      = "defautConfiguration.xml"
    pzInputMxs  = "./scene.mxs"
    pzOutputDir = "./scene"
    
    # camera parameters
    nSteps           = 10           # Number of steps.
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
    
    fStop            = 8            # 8, 11, 16 humman vision
    focalLength      = 35           # 35mm
  
    # 
    # motion parameters
    motion_type = CMotionType.Rotation
    speed = 3.14/(18*3)                 # radius/second
    time = 3                            # motion time
   
    # experiment setting
    obsType = CObservationType.TragetCentered   # "target_center"/ "observer_ceneter"
    minFocalDistance = 0.25                     # the minimal distance between camera to target
    numOfAngles =  3                            # the number of viewpoints for each target 
    numOfObservingDistancesPerAngle = 2         # the number of different camera positions(with different focal distances) in each viewpoint
    numOfTargets = 5                            # the number of targets we will choose for this scene
    
    # task
    task = CTaskType.SetupCamera          # "setup_camera"/ "rendering" / "both"    
    

class CMotionType:
    LinearMotionUpDown = "up->down"
    LinearMotionLeftRight = "left->right"
    RotationClockwise = "Rotate clockwise"
    RotationCounterclockwise = "Ration counterclockwise"

class CTaskType:
    SetupCamera = "setup_camera"
    Rendering = "rendering"
    Both = "both"

class CBBoxConfig:
    BBoxName = "min_box_3dMotionDBSpecial"
    BBoxTopMaterial = "min_box_top_3dMotionDBSpecial"
    BBoxLeftMaterial = "min_box_left_3dMotionDBSpecial"
    BBoxFrontMaterial = "min_box_front_3dMotionDBSpeical"
    
class CObservationType:
    TragetCentered = "target_centered"
    CameraCentered = "camera_centered"
    
    