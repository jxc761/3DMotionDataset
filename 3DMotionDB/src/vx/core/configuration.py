'''
Created on Mar 3, 2014

@author: Jing
'''
from cameraFixParams import CCameraFixParams
from 
class  CSceneType:
    BBoxConstrainted = "scene_with_special_box"
    DotsScene = "dots_scene"
    


class CTaskType:
    SetupCamera = "setup_camera"
    Rendering = "rendering"
    Both = "both"

class CBBoxConfig:
    BBoxName = "<min_box_3dMotionDBSpecial> [0.0.0]"
    BBoxTopMaterial = "min_box_top_3dMotionDBSpecial"
    BBoxLeftMaterial = "min_box_left_3dMotionDBSpecial"
    BBoxFrontMaterial = "min_box_front_3dMotionDBSpecial"
    
class CObservationType:
    TragetCentered = "target_centered"
    CameraCentered = "camera_centered"
    RandomTragetCamera  = "RandomTragetCamera"
    
class CConfiguration(object):
    '''
    classdocs
    '''
    # path configuration
    pzInputMxs  = "/Users/Jing/Workspace/3DMotionDB/input/dots/dots_0/dots_0.mxs"
    pzOutputDir = "/Users/Jing/Workspace/3DMotionDB/output/dots/MXS/dots_0"
    pzOutConf      = "/Users/Jing/Workspace/3DMotionDB/output/dots/MXS/dots_0/configuration.xml"
    
    sceneType = CSceneType.BBoxConstrainted
    #sceneType = CSceneType.DotsScene
    #dotsDistributeBox = [2.0, 2.0, 2.0]               # depth, width, heights 
    
    # camera parameters
    cameraFixParams = CCameraFixParams()
    
    cameraMoveParams = CCameraMoveParams()
    
  
   
    # experiment setting
    minFocalDistance = 1                     # the minimal distance between a camera and a target(the same unit as the model/mesh )
    
    obsType = CObservationType.RandomTragetCamera   # "target_centered"/ "observer_cenetered"
  
   
    # task
    task = CTaskType.SetupCamera          # "setup_camera"/ "rendering" / "both"
    