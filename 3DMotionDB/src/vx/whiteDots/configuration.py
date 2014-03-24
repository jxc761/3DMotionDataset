'''
Created on Feb 18, 2014

@author: Jing
'''
import os

from src.vx.utils import geom as Geom


class CConfiguration(object):
    '''
    classdocs
    '''
   
    '''
    
    def __init__(self, pzOutputDir = "/Users/Jing/Workspace/3DMotionDB/tmp/", 
                 pzMxmDir = "/Users/Jing/Workspace/3DMotionDB/data",
                  numbOfScenes=10, radius= 4e-2, numbOfDots=20, dotsDistributeBox=[2, 2, 2]):
        self.numbOfScene =  numbOfScenes
        self.pzOutputDir = pzOutputDir
        
        
        
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.numbOfScenes = 10
    
        # path setting
        self.pzOutputDir = "/Users/Jing/Workspace/3DMotionDB/tmp/"
        
        self.pzData = "/Users/Jing/Workspace/3DMotionDB/data"
        self.pzSphereMat = os.path.join(self.pzData, "mxm/white_dot.mxm")
        self.pzLightMat = os.path.join(self.pzData, "mxm/white_dots_scene_light.mxm")
        
        
        # sphere setting
        self.radius = 4e-2             # 4cm
        self.numbOfDots = 20   
        self.dotsDistributeBox = [2, 2, 2]  # depth, width, heights 
        
        
        
        
"""

        self.cameraSpace = Geom.CBox([-5, 5, 0], [15, 0, 0], [0, 5, 0], [0, 0, 3])
        
        # light setting
        self.ligthPlane = Geom.CRectangle([15, -5, 0], [0, 15, 3])
        
        # camera positions
      
        # self.sceneBox = [10, 5.0 ,3.0]
        # self.pzScene = os.path.join(self.pzData, "mxs/dots_scene.mxs")
"""