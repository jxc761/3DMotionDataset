'''
Created on Feb 9, 2014

@author: Jing
'''

import os as OS

from configuration import *
import camera as Camera
import shoter as Shoter
import utils.mxs as MXS
import sceneControler as SceneControler

class CGenerator(object):
    '''
    This is the manage to do 
    '''
    

    def __init__(self, conf):

        self.conf = conf
        self.scene = MXS.readMxs(self.pzInputMxs)
        
        
        if conf.sceneType == CSceneType.BBoxConstrainted:
            self.sceneControler = SceneControler.CBBoxSceneControler(self.scene, conf)
        else:
            raise("unknown scene type")
            
        if conf.motionType == CMotionType.Rotation:
            self.camera = Camera.CRotateCamera(conf, self.sceneControler.getZAxis())
        else:
            raise("unknown motion type")
        
        if conf.obsType == CObservationType.TragetCentered:
            self.shooter = Shoter.CTargetCenteredShoter(conf, self.sceneControler, self.camera)
        else:
            raise("unknown observation type")
        
           
    def generate(self):
        self.scripts = self.shooter.genShootScripts()
        for idx in range(self.scripts.count()):  
            pzOutputDir = OS.path.join(self.conf.pzOutputDir, '{:03d}'.format(idx))
            self.__shot(idx, pzOutputDir)
      
      
    def rendering(self):
        self.scene.free()
     

    def __shot(self, idx, pzOutputDir):
        mxScene = self.scene
        idxStr = self.scripts.getIdxStr(idx)
        cameraName = "shot" + idxStr
        
        focalPoint, cameraPos = self.scripts.get(idx)
        self.camera.setup(focalPoint, cameraPos) 
        
        for frameIdx in range(self.camera.getFramesCount()):
            mxCamera = self.camera.instantilize(mxScene, cameraName, frameIdx)
            mxCamera.setActive(True)
            
            pzFile = OS.path.join(pzOutputDir, 'frame_{:03d}.mxs'.format(frameIdx))
            MXS.writeMxs(mxScene, pzFile)
            mxCamera.free()
