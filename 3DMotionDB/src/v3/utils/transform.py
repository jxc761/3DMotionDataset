'''
Created on Feb 9, 2014

@author: Jing
'''
import numpy
import math
import utils
def rotateAroundXAxis(radian):
    cos_r = math.cos(radian)
    sin_r = math.cos(radian)
    
    mtx = numpy.array([[1,     0,      0,  0],
                       [0, cos_r, -sin_r, 0], 
                       [0, sin_r,  cos_r, 0], 
                       [0,     0,      0, 1]],dtype=numpy.double)
    return mtx

def rotateAroundYAxis(radian):
    cos_r = math.cos(radian)
    sin_r = math.cos(radian)
    mtx = numpy.array([[ cos_r, 0, sin_r, 0],
                       [     0, 1,     0, 0], 
                       [-sin_r, 0, cos_r, 0], 
                       [     0, 0,     0, 1]],dtype=numpy.double)
    return mtx

def rotateAroundZAxis(radian):
    cos_r = math.cos(radian)
    sin_r = math.cos(radian)
    mtx = numpy.array([[cos_r, -sin_r, 0, 0], 
                       [sin_r,  cos_r, 0, 0],
                       [    0,      0, 1, 0], 
                       [    0,      0, 0, 1]], dtype=numpy.double)
    return mtx


 
def rotate(center, normal, radian):
    '''
    Refer:
    http://inside.mines.edu/~gmurray/ArbitraryAxisRotation/
    '''
    normal = utils.normalize(normal)

    a = center[0]
    b = center[1]
    c = center[2]
    
    u = normal[0]
    v = normal[1]
    w = normal[2]
    
    u2 = u * u
    v2 = v * v
    w2 = w * w
    
    
    cost = math.cos(radian)
    sint = math.sin(radian)
    rcost = 1 - cost
    
    mtx = numpy.ones([4, 4], dtype=numpy.double)
    mtx[0][0] = u2 + (v2 + w2) * cost
    mtx[0][1] = u * v * rcost - w * sint
    mtx[0][2] = u * w * rcost + v * sint
    mtx[0][3] = (a * (v2 + w2)-u * (b*v + c*w)) * rcost + (b*w-c*v) * sint
    
    mtx[1][0] = u * v * rcost + w * sint
    mtx[1][1] = v2 + (u2 + w2) * cost
    mtx[1][2] = v * w * rcost - u * sint
    mtx[1][3] = (b * (u2 + w2) - v * (a*u+c*w) ) * rcost + (c*u-a*w) * sint
    
    mtx[2][0] = u * w * rcost - v * sint
    mtx[2][1] = v * w * rcost + u * sint
    mtx[2][2] = w2 + (u2 + v2) * cost
    mtx[2][3] = ( c * (u2+v2) - w * (a*u + b*v) ) * rcost + (a*v-b*u) * sint
    
    mtx[3][0] = 0
    mtx[3][1] = 0
    mtx[3][2] = 0
    mtx[3][3] = 1
    
    return mtx

def transform(mtx, point):
    newPoint = numpy.array([0.0, 0.0, 0.0], dtype=numpy.double)
    newPoint[0] =  mtx[0][0] * point[0] + mtx[0][1] * point[1] + mtx[0][2] * point[2] + mtx[0][3] 
    newPoint[1] =  mtx[1][0] * point[0] + mtx[1][1] * point[1] + mtx[1][2] * point[2] + mtx[1][3] 
    newPoint[2] =  mtx[2][0] * point[0] + mtx[2][1] * point[1] + mtx[2][2] * point[2] + mtx[2][3] 
    
    return newPoint
