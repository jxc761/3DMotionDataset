'''
Created on Feb 19, 2014

@author: Jing
'''
import numpy
from numpy import array
import utils as Utils
    
from numpy import math
from math import sin
from math import cos
from math import pi as PI

class CGeom(object):
    def getVertices(self):
        raise("Call an empty function")
      
    
    def getTriangles(self):
        raise("Call an empty function")
    
    def getNormals(self):
        raise("Call an empty function")


def toArray3(pt, dtype = numpy.double):
    return numpy.array([pt[0], pt[1], pt[2]], dtype)

class CParallelogram(CGeom):
    def __init__(self, origin, u, v):
        
        self.origin = toArray3(origin)
        self.u = toArray3(u)
        self.v = toArray3(v)
        normal = numpy.cross(u, v)
        self.normal = Utils.normalize(normal)   
        
    def getVertices(self):
        points = []
        points.append(self.origin)
        points.append(self.origin + self.u)
        points.append(self.origin + self.u + self.v )
        points.append(self.origin + self.v)
        return points
    
    
    def getTriangles(self):
        faces = []
        faces.append(array([0, 1, 2, 0], dtype=numpy.int))
        faces.append(array([2, 3, 0, 0], dtype=numpy.int))
        return faces
    
    def getNormals(self):
        normals = [self.normal]
        return normals
    
    
    
class CRectangle(CParallelogram):
    
    def __init__(self, origin, u, v):
        if numpy.dot(u, v) != 0:
            raise("to construct a rectangle, u and v should be perpendicular")
        super(CRectangle, self).__init__(origin, u, v)
        
        
    def getWidth(self):
        return Utils.norm2(self.u)
    
    
    def getHeight(self):
        return Utils.norm2(self.v)
    
    def getWorldCoord(self, coord):
        u = coord[0]
        v = coord[1]
        
        return self.origin + u * self.u + v * self.v
    
    def getUVCoord(self, coord):
        coord = toArray3(coord)
        p = coord -self.origin
        u = numpy.dot(p, self.u) * (1/self.getWidth())
        v = numpy.dot(p, self.v) * (1/self.getHeight())
        return numpy.array([u, v], dtype=numpy.double)
        
    


class CPrism(object):
    def __init__(self, origin=[0, 0, 0], u=[1, 0, 0], v=[0, 1, 0], w=[0, 0, 1], direction=1):
        self.origin = toArray3(origin)
        self.u = toArray3(u)
        self.v = toArray3(v)
        self.w = toArray3(w)
        self.nw = Utils.norm2( numpy.cross(self.u, self.v) )
        self.nu = Utils.norm2( numpy.cross(self.v, self.w) )
        self.nv = Utils.norm2( numpy.cross(self.w, self.u) )
        
        
    def getVertices(self):
        points = []
        
        points.append(self.origin)
        points.append(self.origin + self.u)
        points.append(self.origin + self.u + self.v )
        points.append(self.origin + self.v)
        
        points.append(self.origin + self.w)
        points.append(self.origin + self.u + self.w)
        points.append(self.origin + self.u + self.v + self.w)
        points.append(self.origin + self.v + self.w)
        
        
        return points
    
    
    def getTriangles(self):
        faces = []
        
        # face 0, 1, 2, 3, -nw
        faces.append(array([0, 1, 2, 5], dtype=numpy.int))
        faces.append(array([2, 3, 0, 5], dtype=numpy.int)) 
      
        #face 4, 5, 6, 7, nw
        faces.append(array([4, 5, 6, 4], dtype=numpy.int))
        faces.append(array([6, 7, 4, 4], dtype=numpy.int))
        
        # face 0, 1, 5, 4, -nv
        faces.append(array([0, 1, 5, 3], dtype=numpy.int))
        faces.append(array([5, 4, 0, 3], dtype=numpy.int))
        
        #face 6, 7, 3, 2, nv
        faces.append(array([6, 7, 3, 2], dtype=numpy.int))
        faces.append(array([3, 2, 6, 2], dtype=numpy.int))
        
        #face 0, 3, 7, 4, -nu
        faces.append(array([0, 3, 7, 1], dtype=numpy.int))
        faces.append(array([7, 4, 0, 1], dtype=numpy.int))
        
        #face 5, 6, 2, 1, nu
        faces.append(array([5, 6, 2, 0], dtype=numpy.int))
        faces.append(array([2, 1, 5, 0], dtype=numpy.int))
        return faces
    
    def getNormals(self):
        nu = self.direction * Utils.normalize(self.u)
        nv = self.direction * Utils.normalize(self.v)
        nw = self.direction *Utils.normalize(self.w)
        normals = [nu, -1 *nu, nv, -1*nv, nw, -1*nw]
        return normals
    
    
    
class CBox(CPrism):   
    def __init__(self, origin=[0, 0, 0], u=[1, 0, 0], v=[0, 1, 0], w=[0, 0, 1], direction = 1):
        
        if numpy.dot(u, v) != 0 or numpy.dot(v, w) != 0 or numpy.dot(w, u) != 0:
            raise("to construct a box, u, v and w should be perpendicular")
        
        super(CBox, self).__init__(origin, u, v, w, direction)
        
    def getDepth(self):
        return Utils.norm2(self.u)
    
    def getWidth(self):
        return Utils.norm2(self.v)
    
    def getHeight(self):
        return Utils.norm2(self.w)
    
    def getWorldCoord(self, coord):
        u = coord[0]
        v = coord[1]
        w = coord[2]
        
        return self.origin + u * self.u + v * self.v + w * self.w

    def getUVWCoord(self, coord):
        p = toArray3(coord) -self.origin
        u = numpy.dot(p, self.u) * (1/self.getDepth())
        v = numpy.dot(p, self.v) * (1/self.getWidth())
        w = numpy.dot(p, self.w) * (1/self.getWidth())
        return numpy.array([u, v, w], dtype=numpy.double)


class CSphere(CGeom):
    
    def __init__(self, origin=[0, 0, 0], r=1.0, nDiv1 = 36, nDiv2 = 24):
        self.origin = toArray3(origin)
        self.r = r
        # theta the angle between the vector with the projection of it
        # phi   the angle between the projection with x axis 
        self.nDivTheta = nDiv1
        self.nDivPhi  = nDiv2
             
    def getVertices(self):
        points = getNormalSphere(self.nDivTheta, self.nDivPhi)
        newPoints = []
        for pt in points:
            newPt = pt * self.r + self.origin
            newPoints.append(newPt)
            
        return newPoints 
      
       
    
    def getTriangles(self):
     
        triangles = []
        N = (self.nDivTheta - 1 )* self.nDivPhi + 2
        # the first level
        paId = self.nDivPhi * (self.nDivTheta - 1)
        for j in range(self.nDivPhi):
            pbId = j
            pcId = (j+1) % self.nDivPhi
            assert(paId < N and pbId < N and pcId < N)
            triangle = numpy.array([paId, pbId, pcId, paId, pbId, pcId])
            triangles.append(triangle)
        
        # the middle levels    
        for i in range(self.nDivTheta-2):
            for j in range(self.nDivPhi):
                pt1 = i * self.nDivPhi + j
                pt2 = i * self.nDivPhi + (j + 1) % self.nDivPhi
                pt3 = pt1 + self.nDivPhi
                pt4 = pt2 + self.nDivPhi
                
                assert(pt1 < N and pt2 < N and pt3 < N and pt4 < N)
                triangle1 = numpy.array([pt1, pt2, pt3, pt1, pt2, pt3])
                triangle2 = numpy.array([pt2, pt3, pt4, pt2, pt3, pt4])
                triangles.append(triangle1)
                triangles.append(triangle2) 
                
        # the last level
        # for each level there are self.nDivPhi points
        # before the last level, there are self.nDivTheta - 1 full level, and one polar point
        paId = self.nDivPhi * (self.nDivTheta - 1) + 1 # the point's idx
        offset = self.nDivPhi *  (self.nDivTheta - 2)
        for j in range(self.nDivPhi):
            pbId = offset + j
            pcId = offset + (j + 1) % self.nDivPhi
            assert(paId < N and pbId < N and pcId < N)
            triangle = numpy.array([paId, pbId, pcId, paId, pbId, pcId])
            triangles.append(triangle)
            
        return triangles
    
    def getNormals(self):
        return getNormalSphere(self.nDivTheta, self.nDivPhi)
    
    
def getNormalSphere(nDivTheta, nDivPhi):  
        dTheta = PI/nDivTheta
        dPhi =  2*PI/nDivPhi
        points = []
        

        for i in range(1, nDivTheta):
            for j in range(nDivPhi):
                theta =  -PI/2 + dTheta * i
                phi = j * dPhi

                x = cos(theta) * cos(phi)
                y = cos(theta) * sin(phi)
                z = sin(theta)
                pt = toArray3([x,y,z])
                points.append(pt)
                
        # two polar points
        points.append(toArray3([0, 0, -1]))      
        points.append(toArray3([0, 0, 1]))
        assert ( len(points) == ( (nDivTheta - 1 )* nDivPhi + 2) )
        return points  
    
"""
        # theta xy-plane
        # phi  x-axis  
        # x = xo + r cos(theta) cos(phi)
        # y = yo + r cos(theta) sin(phi)
        # z = zo + r sin(theta)
"""