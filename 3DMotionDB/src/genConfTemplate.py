'''
Created on Feb 17, 2014

@author: Jing
'''
import sys
from vx.configuration import CConfiguration


def usage():
    print("usage: {} [configuration file]".format(__file__))
    
def main(argv):
    usage()
    if len(argv) < 1:                         
        sys.exit(2)
        
    conf = CConfiguration()
    conf.save(argv[0])
    
if __name__ == '__main__':
    main(sys.argv[1:])