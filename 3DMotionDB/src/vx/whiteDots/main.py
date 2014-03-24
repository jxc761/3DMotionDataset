'''
Created on Feb 20, 2014

@author: Jing
'''

from configuration import CConfiguration
from dotsGenerator import CDotsGenerator

if __name__ == '__main__':
    conf = CConfiguration()
    generator = CDotsGenerator(conf)
    generator.generate()