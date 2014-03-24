'''
Created on Feb 9, 2014

@author: Jing
'''
import random
import numpy
import math
    
def norm2(v):

    return math.sqrt(v[0]*v[0] + v[1] * v[1] + v[2] * v[2])

def normalize(v):
    nv = numpy.array(v, dtype=numpy.float32) / norm2(v)
    return nv

def distance(v1, v2):
    d1 = v1[0] - v2[0] 
    d2 = v1[1] - v2[1]
    d3 = v1[2] - v2[2]
    return math.sqrt(d1*d1 + d2 * d2 + d3 * d3)

def isHitTriangle(pe, vd, pa, pb, pc, minT, maxT):
    '''
    Method: IsHitTriangle(pe, vd, pa, pb, pc, minT, maxT) -> (isHit, t)
    Description: check whether the line segment pe + t vd ( minT <= t <= maxT)hit the triangle <pa, pb, pc> 
    '''
    a = pa[0] - pb[0]
    b = pa[1] - pb[1]
    c = pa[2] - pb[2]
    
    d = pa[0] - pc[0]
    e = pa[1] - pc[1]
    f = pa[2] - pc[2]
    
    g = vd[0]
    h = vd[1]
    i = vd[2]
    
    j = pa[0] - pe[0]
    k = pa[1] - pe[1]
    l = pa[2] - pe[2]
    
    f1 = e * i - h * f
    f2 = g * f - d * i
    f3 = d * h - e * g
    
    f4 = a * k - j * b
    f5 = j * c - a * l
    f6 = b * l - k * c
    
    M = a * f1 + b * f2 + c * f3
    
    if M == 0 : # no solution
        return (False, 0)
    
    t = - (f* f4 + e * f5 + d * f6) / M
    
    if t < minT or t > maxT:
        return (False, t)
    
    gamma = (i * f4 + h * f5 + g * f6) / M
    if gamma < 0 or gamma > 1:
        return (False, t)
    
    beta = (j * f1 + k * f2 + l * f3) / M
    if beta < 0 or beta > 1-gamma:
        return (False, t)
    
    return (True, t)

     
def rayIntersectObject(pt, vd, faces, points, tMin, tMax):
    isHit = False
    hitT = False
    for fId in range(len(faces)):
        pa = points[faces[fId][0]]
        pb = points[faces[fId][1]]
        pc = points[faces[fId][2]]
        isIntersect, t = isHitTriangle(pt, vd, pa, pb, pc, tMin, tMax)
        if isIntersect:
            isHit = True
            hitT = t
            tMax = t
    return (isHit, hitT)


def rayIntersectObjects(pt, vd, facesList, pointsList, tMin, tMax):
    assert(len(facesList) == len(pointsList))
    isHit = False
    hitT = False
    for objId in range(len(pointsList)):
        faces = facesList[objId]
        points = pointsList[objId]
        isIntersect, t = rayIntersectObject(pt, vd, faces, points, tMin, tMax)
        if isIntersect:
            isHit = True
            tMax = t
            hitT = t
               
    return (isHit, hitT)

