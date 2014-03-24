'''
Created on Feb 9, 2014

@author: Jing
'''
import xml.etree.ElementTree as xmlElementTree
from xml.etree.ElementTree import Element, SubElement #, ElementTree, dump, tostring
import xml.dom.minidom as MiniDom
import types as Types

class  CSceneType:
    BBoxConstrainted = "scene_with_special_box"
    DotsScene = "dots_scene"
    
class CMotionType:
    
    Rotation = "rotation"
    '''
    LinearMotionUpDown = "up->down"
    LinearMotionLeftRight = "left->right"
    RotationClockwise = "Rotate clockwise"
    RotationCounterclockwise = "Ration counterclockwise"
    '''

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
    
    #sceneType = CSceneType.BBoxConstrainted
    sceneType = CSceneType.DotsScene
    dotsDistributeBox = [2.0, 2.0, 2.0]               # depth, width, heights 
    
    # camera parameters
    nSteps           = 1            # Number of steps.
    shutter          = 1/125.0      # Camera shutter (1/s).
    filmWidth        = 36e-3           # Camera film width (mm).
    filmHeight       = 24e-3           # Camera film height (mm).
    iso              = 100          # Camera ISO.

    pDiaphragmType   = "CIRCULAR"   # Diaphragm type. Possible values: "CIRCULAR" and "POLYGONAL".
    angle            = 0            # Shutter angle.
    nBlades          = 0            # Number of diaphragm blades if pDiaphragmType is "POLYGONAL".
    
    fps              = 24           # Frames per second.
    xRes             = 96           # Resolution output width.
    yRes             = 64           # Resolution output height.
    pixelAspect      = 1.0          # Pixel aspect ratio.
    projectionType   = 0            # Camera projection type. 0 (perspective, default), 
                                    # 1 (front), 2 (top), 3 (left), 4 (back), 5 (bottom), 6 (right).   
    focalLengthNeedCorrection=True  # Indicates whether focal length needs correction. Default value: 1 (true).
    
    fStop            = 5.6           # 8, 11, 16 humman vision / 2.8 dark, 5.6 / 8 day light 
    fieldOfView      = 3.14 / 3      # radius
    
    # 
    # motion parameters
    motionType = CMotionType.Rotation
    speed = 3.14/(12*3)                 # radius/second
    time = 3                            # motion time (second)
   
    # experiment setting
    minFocalDistance = 1                     # the minimal distance between a camera and a target(the same unit as the model/mesh )
    
    obsType = CObservationType.RandomTragetCamera   # "target_centered"/ "observer_cenetered"
    numbOfViews     = 2                            # the number of viewpoints for each target 
    numbOfCameras   = 3                     # the number of camera positions in each viewpoints -> name change
    numbOfTargets   = 3                           # the number of targets we will choose for this scene 
   
    # task
    task = CTaskType.SetupCamera          # "setup_camera"/ "rendering" / "both"
    
    def save(self, pzFile):
        root = Element("configuration") 
        attributes = dir(self)
        for attrName in attributes:
            if attrName.startswith("_"):
                continue
            value = getattr(self, attrName)
            attrType = "string"
            if type(value) == Types.IntType:
                attrType = "int"
            elif type(value) == Types.FloatType:
                attrType = "float"
            elif type(value) ==  Types.MethodType:
                continue
            else:
                pass
        
            subElem  = SubElement(root, attrName)
            subElem.text = str(value)
            subElem.attrib["type"] = attrType
    
        # save out the configuration      
        doc = MiniDom.parseString(xmlElementTree.tostring(root))
        prettyxml = doc.toprettyxml(indent="   ", newl="\r\n") #  encoding='utf-8'
        file_object = open(pzFile, "w")
        file_object.write(prettyxml)
        file_object.close()
        #print(prettyxml)
       
    def load(self, pzFile):
        tree = xmlElementTree.parse(pzFile)
        root = tree.getroot()
        
        attributes = dir(self)
        for attrName in attributes:
            if attrName.startswith("_"):
                continue
            value = getattr(self, attrName)
            if type(value) ==  Types.MethodType:
                continue
            
            elem = root.find(attrName)
            if elem == None:
                print("no element for attribute: " + attrName)
            
            value = elem.text
            attType = elem.attrib['type']

            if attType == "int":
                value = int(value)
            elif attType == "float":
                value = float(value)
            elif attType == "string":
                value = str(value)
            else:
                print("unkonw type")
                continue
            
            setattr(self, attrName, value)
        
    

    
    
        