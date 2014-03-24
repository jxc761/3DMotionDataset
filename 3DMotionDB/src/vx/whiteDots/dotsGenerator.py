'''
Created on Feb 18, 2014

@author: Jing
'''


from pymaxwell import *

from vx.utils import geom as Geom
from vx.utils import mxs as MXS
import numpy.random as random
import os
import shutil

class CDotsGenerator(object):
    
    
    def __init__(self, conf):
        self.radius = conf.radius
        self.pzSphereMat = conf.pzSphereMat
        self.pzLightMat = conf.pzLightMat
        
        self.pzOutputDir = conf.pzOutputDir
        self.numbOfDots = conf.numbOfDots
        self.numbOfScenes = conf.numbOfScenes
        
        self.depth  = conf.dotsDistributeBox[0]
        self.width  = conf.dotsDistributeBox[1]
        self.height = conf.dotsDistributeBox[2]
        
        if (os.path.isdir(self.pzOutputDir)):
            print(self.pzOutputDir + "exits, we will remove all contents under it")
            shutil.rmtree(self.pzOutputDir)
            
        os.mkdir(self.pzOutputDir)
        
    def generate(self):
        
        
        for iscene in range(self.numbOfScenes):
            pzSubDir = os.path.join(self.pzOutputDir, "dots_{}".format(iscene))
            os.mkdir(pzSubDir)
            pzOutFile  = os.path.join(pzSubDir, "dots_{}.mxs".format(iscene))
            
            scene = self.create_scene()
            
            # generate dots
            self.scatter_sphere(scene)
        
            # build light_plane
            self.create_light_planes(scene)
            
            
            
            scene.writeMXS(pzOutFile)
            scene.freeScene()
            
            print("Generate scene: " + pzOutFile)
        
        print("finish generation!")
        
        
        
    def create_scene(self):
        # Add the sphere to the new sphere
        scene = Cmaxwell(mwcallback)
       
        # turn off environment lighting
        env = scene.getEnvironment()
        env.enableEnvironment(False)

        return scene
    
    def scatter_sphere(self, scene):
            
        # Add a new material to the sphere
        mat = scene.readMaterial(self.pzSphereMat)
        mat = scene.addMaterial(mat)
        
        radius = self.radius
        
        
        # scatter dots into scenes
        for i in range(self.numbOfDots):
            # Create a instance of the sphere in the scene
            x = random.random() * self.depth - self.depth/2
            y = random.random() * self.width - self.width/2
            z = random.random() * self.height - self.height/2
            
            dot = Geom.CSphere([x, y, z], radius)
            points = dot.getVertices()
            normals = dot.getNormals()
            triangles = dot.getTriangles()
            obj = MXS.createMxObject(scene, "dot_{}".format(i), points, normals, triangles)

            # Assign the material to the object of the new sphere
            obj.setMaterial(mat)
          
            
    def create_light_planes(self, scene):
        distance = self.depth * 3
        height = self.height * 3
        width = self.width * 3

        origin = [distance, -width/2, -height/2]
        v = [0, width , 0]
        u = [0, 0, height]
      
    
        plane = Geom.CRectangle(origin, u, v)
        points = plane.getVertices()
        triangles = plane.getTriangles()
        normals = plane.getNormals()

        lightPlane = MXS.createMxObject(scene, "light_plane", points, normals, triangles)
        lightMat = scene.readMaterial(self.pzLightMat)
        lightMat = scene.addMaterial(lightMat)
        lightPlane.setMaterial(lightMat)
        lightPlane.setHideToCamera(True)
        lightPlane.setHideToGI(True)
        lightPlane.setHideToReflectionsRefractions(True)
        
        '''
        origin = [-distance, -width/2, -height/2]
        u = [0, width , 0]
        v = [0, 0, height]

    
        plane = Geom.CRectangle(origin, u, v)
        points = plane.getVertices()
        triangles = plane.getTriangles()
        normals = plane.getNormals()

        MXS.createMxObject(scene, "plane", points, normals, triangles)
            
        #MXS.setObjectInvisible(lightPlane)
        '''
  

