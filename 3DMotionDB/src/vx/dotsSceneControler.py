'''
Created on Feb 20, 2014

@author: Jing
'''

from sceneControler import CSceneControler
from random import random
from utils import mxs as MXS
from utils.geom import CBox
from numpy import array

class CDotsSceneControler(CSceneControler):
    
    # test can we put a camera at the point
    def __init__(self, mxScene, conf):
        '''
        Constructor
        '''
        self.scene = mxScene
        self.conf = conf
        self.pointsList, self.facesList, self.namesList = MXS.getObjectGeometris(mxScene)
        
        distance    = conf.dotsDistributeBox[0]/2 + conf.minFocalDistance
        depth       = conf.dotsDistributeBox[0] * 1.5
        width       = conf.dotsDistributeBox[1] * 1.5
        height      = conf.dotsDistributeBox[2] * 1.5
        
        origin = [distance, -width/2, -height/2 ]
        u = [depth, 0, 0]
        v = [0, width, 0]
        w = [0, 0, height]
        self.box = CBox(origin, u, v, w)
    
    def isLegalCameraPosition(self, point): 
        return True
        
    def randPickPoint(self):
        u = random() 
        v = random() 
        w = random()
        return self.box.getWorldCoord((u, v, w))
    
    def getZAxis(self):
        return array([0.0, 0.0, 1.0])
    
        