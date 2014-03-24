'''
Created on Feb 9, 2014

@author: Jing
'''


from randShoter import CRandShoter
from dotsSceneControler import CDotsSceneControler
from src.vx import *
from targetCenteredShoter import *

from configuration import *
import camera as Camera
import shoter as Shoter
import sceneControler as SceneControler
import shutil as ShUtil

import os as Os
from pymaxwell import *
import utils.mxs as MXS
    
def generate(conf):
    

    install_generator(conf)
    
    #read in the scene 
    mxsName = Os.path.basename(conf.pzInputMxs)
    pzInputMxs = Os.path.join(conf.pzOutputDir, mxsName)
    scene = MXS.readMXS(pzInputMxs)
    
    # initialize
    if conf.sceneType == CSceneType.BBoxConstrainted:
        sceneControler = SceneControler.CBBoxSceneControler(scene, conf)
    elif conf.sceneType == CSceneType.DotsScene:
        sceneControler = CDotsSceneControler(scene, conf)
    else:
        raise("unknown scene type")
        
    if conf.motionType == CMotionType.Rotation:
        camera = Camera.CRotateCamera(conf, sceneControler.getZAxis())
    else:
        raise("unknown motion type")
    
    if conf.obsType == CObservationType.TragetCentered:
        shooter = CTargetCenteredShoter(conf, sceneControler, camera)
    elif conf.obsType == CObservationType.RandomTragetCamera:
        shooter = CRandShoter(conf, sceneControler, camera)
    else:
        raise("unknown observation type")
    
    print("Begin generate shooting script, plase wait....")
    # shot
    scripts = shooter.genShotScripts()
    
    print("Begin instantilize maxwell camera, pleas wait")
    
    for idx in range(scripts.count()):
        curCamera = scripts.get(idx)
        idxStr = scripts.getIdxStr(idx)
        pzCurOutputMxs = Os.path.join(conf.pzOutputDir, "obs_" + idxStr + ".mxs")
        pzCurOutputDir = Os.path.join(conf.pzOutputDir, "obs_" + idxStr)
        
        instantiate_observation(camera, pzInputMxs, pzCurOutputMxs)
        #instantiate_frames(camera, pzInputMxs, pzCurOutputDir)
        
    scene.freeScene()
    
    
    
#########################################
# Method to instantiate the observation
#########################################    
def instantiate_observation(camera, pzInputMxs, pzOutputMxs):
    """ copy ``pzInputMxs`` to ``pzOutputMxs`` and create a sequence of maxwell cameras in pzOutputMxs according to ``camera``
        
    Methods: instantiate_observation(CCamera camera, str pzInputMxs, str pzOutputMxs)
        
    Args:
        camera(CCamera): which to be instantiate
        pzInputMxs(str): the source path of the original maxwell scene file
        pzOutputMxs(str): the destination of the output maxwell scene file
        
    Note:
        * If the file of pzOutputMxs exists, it will be deleted except it is the same as pzInputMxs
        * It is highly recommended that the output file differ from the input file
    """
    
    if pzInputMxs != pzOutputMxs:
        if Os.path.isfile(pzOutputMxs):
            print("Follwoing file exists: " + pzOutputMxs)
            print("We will remove it")
            ShUtil.rmtree(pzOutputMxs)
        
        ShUtil.copy(pzInputMxs, pzOutputMxs)
    
    curScene = MXS.readMXS(pzInputMxs)
    for frameIdx in range(camera.getFramesCount()):
        cameraName = "frame{}".format(frameIdx)
        camera.instantilize(curScene, cameraName, frameIdx)
        
    set_render_parameters(curScene, Os.path.basename(pzOutputMxs) )
    MXS.writeMXS(curScene, pzOutputMxs)
    curScene.freeScene()
    
    
def instantiate_frames(camera, pzInputMxs, pzOutputDir):
    if Os.path.isdir(pzOutputDir):
        print("Following directory exists: " + pzOutputDir)
        print("We will remove the content under it")
        ShUtil.rmtree(pzOutputDir)
        
    Os.mkdir(pzOutputDir)
    
    for frameIdx in range(camera.getFramesCount()):
        pzCurFile = Os.path.join(pzOutputDir, "frame{}.mxs".format(frameIdx))
        ShUtil.copy(pzInputMxs, pzCurFile)
        curScene = MXS.readMXS(pzCurFile)
        cameraName = "camera"
        camera.instantilize(curScene, cameraName, frameIdx)
        set_render_parameters(curScene)
        MXS.writeMXS(curScene, pzCurFile)
        curScene.freeScene()

    
######################
########################    
def set_render_parameters(scene, searchPath):

    scene.setRenderParameter("SAMPLING LEVEL", 16)
    scene.setRenderParameter('DO MOTION BLUR', 0)
    scene.setRenderParameter('DO DISPLACEMENT', 0)
    scene.setRenderParameter('DO DISPERSION', 0)
    scene.addSearchingPath(searchPath)

def install_generator(conf):
    pzInputMxs = conf.pzInputMxs
    pzOutputDir = conf.pzOutputDir
    
    pzInputDir = Os.path.dirname(pzInputMxs)
    
    if Os.path.isdir(pzOutputDir):
        print("Following directory exists: " + pzOutputDir)
        #choice = raw_input("We will remove all content in this directory. Are you sure to continue[y/n]:")
        choice = 'y'
        if choice == 'n' or choice == 'N':
            sys.exit("Install process stops!")
        ShUtil.rmtree(pzOutputDir)
    else:
        print("Following path does not exist: " + pzOutputDir)
        print("We will create it.")
        
        
    ShUtil.copytree(pzInputDir, pzOutputDir, symlinks=False)
    conf.save(conf.pzOutConf)
