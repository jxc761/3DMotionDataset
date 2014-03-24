'''
Created on Mar 3, 2014

@author: Jing
'''
from configuration import *
from generator import generate

def main():
    conf = CConfiguration()
    conf.pzInputMxs = "/Users/Jing/Workspace/3DMotionDB/input/scenes/LivingRoom02/living_room_02.mxs"
    conf.pzOutputDir = "/Users/Jing/Workspace/3DMotionDB/output/exp030414"
    conf.pzOutConf = "/Users/Jing/Workspace/3DMotionDB/output/exp030414/configuration.xml"
    
    conf.obsType = CObservationType.TragetCentered
    conf.numbOfCameras = 2
    conf.numbOfTargets = 3
    conf.numbOfViews = 2
    
    conf.sceneType = CSceneType.BBoxConstrainted
    conf.motionType = CMotionType.Rotation
    conf.minFocalDistance = 0.4 
    
    conf.fps = 24
    conf.xRes = 288
    conf.yRes = 192
    
    print("begin generation")
    generate(conf)
    print("finish generation")
    
if __name__ == '__main__':
    main()
    pass