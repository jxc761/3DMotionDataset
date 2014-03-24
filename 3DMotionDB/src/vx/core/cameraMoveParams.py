'''
Created on Mar 3, 2014

@author: Jing
'''

class CMotionType:
    
    Rotation = "rotation"
    '''
    LinearMotionUpDown = "up->down"
    LinearMotionLeftRight = "left->right"
    RotationClockwise = "Rotate clockwise"
    RotationCounterclockwise = "Ration counterclockwise"
    '''
    
class CCameraMoveParams(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        self.motionType = CMotionType.Rotation
        self.speed      = 3.14/(12*3)                   # radius/second
        self.time       = 3                             # motion time (second)
        self.numbOfViews     = 2                        # the number of viewpoints for each target 
        self.numbOfCameras   = 2                        # the number of camera positions in each viewpoints -> name change
        self.numbOfTargets   = 2                        # the number of targets we will choose for this scene    
