'''
Created on Feb 17, 2014

This is the entry function for 3d motion data base generation.


@author: Jing
'''
import sys

from vx.configuration import CConfiguration
from vx.generator import generate

def usage():
    print("usage: {} [configuration file]".format(__file__))
    print("examples")
    print(__file__)
    print("  :generate data with the default configuration defined in configuration.py")
    print(__file__ + " configuration.xml")
    print("  :generate data with the default configuration defined in configuration.xml")

def main(argv):
    usage()
    if len(argv) > 1:                         
        sys.exit(2)
    
     
    conf = CConfiguration()
    if len(argv) == 1:
        print("load in configuration")
        conf.load(argv[0])
        print("finish loading")
        
    print("begin to generate data")
    generate(conf)
    print("finish generation")
   

def shot_dots():
    
    for i in range(10):
        conf = CConfiguration()
        conf.pzInputMxs = "/Users/Jing/Workspace/3DMotionDB/tmp/dots_{}/dots_{}.mxs".format(i, i)
        conf.pzOutputDir = "/Users/Jing/Workspace/3DMotionDB/output/dots/dots_{}".format(i)
        conf.pzOutConf = "/Users/Jing/Workspace/3DMotionDB/output/dots/dots_{}/configuration.xml".format(i)
        
        generate(conf)
        
if __name__ == '__main__':    
    #main(sys.argv[1:])
    shot_dots()
    