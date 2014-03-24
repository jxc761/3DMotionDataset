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
   
        

    def __init__(self):
        '''
        Constructor
        '''
        self.numbOfScenes = 10
        

        # path setting
        self.pzOutputDir = "/Users/Jing/Workspace/3DMotionDB/output/black_dots"
        
        self.pzData = "/Users/Jing/Workspace/3DMotionDB/input"
        self.pzSphereMat = os.path.join(self.pzData, "mxm/black_dot.mxm")
        self.pzLightMat = os.path.join(self.pzData, "mxm/black_dots_scene_light.mxm")
        self.pzPlaneMat = os.path.join(self.pzData, "mxm/black_dots_scene.mxm")
        
        
        # sphere setting
        self.radius = 2.0             # 2cm
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