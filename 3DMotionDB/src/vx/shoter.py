'''
Created on Feb 12, 2014

@author: Jing
'''

#from sceneControler import *

class CShotScripts:
    """ This is the interface of a set of shot scripts. 
    
    It works like a shooting schedule. It contains several shoot script. Each script can be used to 
    guide one time shoot. 
     
    An example:
        for idx in range( script.count() ):
            idxStr = scripts.getIdxStr(idx)
            camera = scripts.get(idx)
            do something using ``idxStr`` and ``camera`` 
    """
    
    def __init__(self):
        pass
    
    def getIdxStr(self, idx):
        """ Return an string to specify the idx-th shot
        
        Args:
            idx (int) : the idx of the script 
        
        Returns:
            a string to specify the idx-th shot
        """
        pass
    
    def get(self, idx):
        """ Return the idx-th camera which has been set up."""
        pass
    
    def count(self):
        """Return the total number of scripts."""
        pass
        
class CShoter(object):
    """This interface works like a screenwriter who can make a shot schedule. 
    
    It can work out/create the shot scripts, i.e. an object of CShotScripts
    
     
    """
    def __init__(self, conf, sceneControler, camera):
        '''
        Constructor
        '''
        self.sceneControler = sceneControler
        self.camera = camera
        
    def genShotScripts(self):
        print "This is an interface. It can not be used!"
        pass



