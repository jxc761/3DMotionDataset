'''
Created on Feb 14, 2014

@author: Jing
'''

from pymaxwell import *
import os as Os
import shutil as ShUtil

def genScenePreview(pzInputDir, pzOutputDir):
    mxslist = getFilesFromPath(pzInputDir,'mxs')
    
    
    # Read each MXS and print some info
    for file in mxslist:
        pzMxs = Os.path.join(pzInputDir, file)     
        print(pzMxs)  
        sceneName = getSceneName(pzMxs)
        pzImg = Os.path.join(pzOutputDir, sceneName + ".jpg") 
        pzMxi = Os.path.join(pzOutputDir, sceneName + ".mxi") 
    
        parameters = []
        parameters.append('-mxs:' + pzMxs) 
        parameters.append('-o:' + pzImg) 
        parameters.append('-mxi:' + pzMxi)
        parameters.append('-res:300x200')
        parameters.append('-time:10')
        parameters.append('-sl:5')
        parameters.append('-nowait')
        parameters.append('-verbose:0')
        runMaxwell(parameters)
        
def getSceneName(path):
    root, ext = Os.path.splitext(path)
    sceneName = Os.path.basename(root)
    return sceneName


if __name__ == "__main__":
    pzInputDir  = "/Users/Jing/Workspace/3DMotionDB/output/MXS/TestScene"
    pzOutputDir = "/Users/Jing/Workspace/3DMotionDB/output/MXS/TestScene/preview"
    if Os.path.exists(pzOutputDir):
        ShUtil.rmtree(pzOutputDir)
    Os.mkdir(pzOutputDir)
    
    genScenePreview(pzInputDir, pzOutputDir)
    