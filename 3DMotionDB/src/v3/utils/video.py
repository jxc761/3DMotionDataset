'''
Created on Feb 26, 2014

@author: Jing
'''
import shutil
import os

import subprocess


def upsampleFrames(startId, stopId, dstStartId, pzInputDir, pzDstDir, rate=2):
    frameNumb = stopId - startId + 1
    for offset in range(0, frameNumb):
        i = startId + offset
        src = os.path.join(pzInputDir, "frame{:03d}.jpg".format(i))
        for k in range(0, rate):
            j = dstStartId + offset * rate + k
            dst = os.path.join(pzDstDir, "frame{:03d}.jpg".format(j))
            shutil.copyfile(src, dst)
    
    nextDstFrameId = dstStartId + frameNumb * rate 
    return nextDstFrameId


def revertFrames(startId, stopId, dstStartId, pzInputDir, pzDstDir):
    numb = stopId-startId+1
    for offset in range(0,numb):
        i = startId + offset
        j = dstStartId + (numb-1 - offset)
        src = os.path.join(pzInputDir, "frame{}.jpg".format(i))
        dst = os.path.join(pzDstDir, "frame{:03d}.jpg".format(j))
        shutil.copyfile(src, dst)
        
    nextDstFrameId = dstStartId + numb
    return nextDstFrameId

def repeatFrames(startId, stopId, dstStartId, pzInputDir, pzDstDir):
    numb = stopId-startId+1
    for offset in range(0,numb):
        i = startId + offset
        j = dstStartId + offset
        src = os.path.join(pzInputDir, "frame{}.jpg".format(i))
        dst = os.path.join(pzDstDir, "frame{:03d}.jpg".format(j))
        shutil.copyfile(src, dst)
        
    nextDstFrameId = dstStartId + numb
    return nextDstFrameId
    
def repeatFrame(frameId, numb, dstStartId, pzInputDir, pzDstDir):
    
    src = os.path.join(pzInputDir, "frame{}.jpg".format(frameId))
    for i in range(0, numb):
        j = dstStartId + i
        dst = os.path.join(pzDstDir, "frame{:03d}.jpg".format(j))
        shutil.copyfile(src, dst)
        
    nextDstFrameId = dstStartId + numb
    return nextDstFrameId

def build(pzInputDir, pzOutputDir):
    shutil.rmtree(pzOutputDir)
    os.mkdir(pzOutputDir) 

    startId=0
    stopId= 71

    repeatFrames(startId, stopId, 0, pzInputDir, pzOutputDir)
    
def buildRound(pzInputDir, pzOutputDir):
    shutil.rmtree(pzOutputDir)
    os.mkdir(pzOutputDir) 

    
    startId=0
    stopId= 71

    nextId = repeatFrames(startId, stopId, 0, pzInputDir, pzOutputDir)
    nextId = repeatFrame(stopId,  10, nextId, pzInputDir, pzOutputDir)
    nextId = revertFrames(startId, stopId, nextId, pzInputDir, pzOutputDir)
    nextId = repeatFrame(startId, 10, nextId, pzInputDir, pzOutputDir)
   
def buildLong(pzInputDir, pzOutputDir):
    shutil.rmtree(pzOutputDir)
    os.mkdir(pzOutputDir) 

    
    startId=0
    stopId= 71

    nextId = repeatFrames(startId, stopId, 0, pzInputDir, pzOutputDir)
    nextId = repeatFrame(stopId,  10, nextId, pzInputDir, pzOutputDir)
    nextId = revertFrames(startId, stopId, nextId, pzInputDir, pzOutputDir)
    nextId = repeatFrame(startId, 10, nextId, pzInputDir, pzOutputDir)
    
    startId = 0
    stopId =nextId -1
    
    nextId = upsampleFrames(startId, stopId, nextId, pzOutputDir, pzOutputDir, 2)

if __name__ == "__main__":
    pzTempDir = "/Users/Jing/Workspace/temp"
    pzOutputDir="/Users/Jing/Workspace/videos"
    argInput= pzTempDir + "/frame%03d.jpg"
    #shutil.rmtree(pzOutputDir)
    os.mkdir(pzOutputDir)
    for dotsId in range(3, 9):
        for eId in range(0, 3):
            for tId in range(0, 3):
                for dId in range(0, 2):
                    name = "dots{}_e{}_t{}_d{}".format(dotsId, eId, tId, dId)
                    pzInputDir = "/Users/Jing/Workspace/outputs/" + name
                   
                    build(pzInputDir, pzTempDir)
                    argOutput = pzOutputDir + "/" + name + "_org.mpg"
                    subprocess.call(['/Users/Jing/Research/3DMotionDB/libs/ffmpeg', '-f', 'image2', '-i', argInput, '-r', '24', argOutput])
                    
                    buildRound(pzInputDir, pzTempDir)
                    argOutput = pzOutputDir + "/" + name + "_round.mpg"
                    subprocess.call(['/Users/Jing/Research/3DMotionDB/libs/ffmpeg', '-f', 'image2', '-i', argInput, '-r', '24', argOutput])
                    
                    buildLong(pzInputDir, pzTempDir)
                    argOutput = pzOutputDir + "/" + name + "_long.mpg"
                    subprocess.call(['/Users/Jing/Research/3DMotionDB/libs/ffmpeg', '-f', 'image2', '-i', argInput, '-r', '24', argOutput])
    