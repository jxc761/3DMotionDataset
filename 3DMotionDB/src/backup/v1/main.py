'''
Created on Feb 3, 2014

@author: Jing
'''
from Experimenter import CExperimenter

from pymaxwell import *
from Configuration import *


def run(config):
    exp = CExperimenter(config)
    
if __name__ == '__main__':
    config = CConfig
    run(config)
    

"""
def SetupCamera(config):
    pzMxs = config.pzInputMxs
    scene = Cmaxwell(mwcallback)
    ok = scene.readMXS(pzMxs)
    if not ok:
        raise "unable to open file: " + pzMxs
    
    exp = CExperimenter(scene, config)
    exp.do()
    scene.freeScene()
    

def Rendering(config):
    
    
    pass


def run(config):
    '''
    run(CConfig config)
    '''
    if config.task != CTaskType.Rendering:
        SetupCamera(config)
    elif config.task != CTaskType.SetupCamera:
        Rendering(config)
    else:
        pass
    
    print "finish the task: " + config.task
    

"""