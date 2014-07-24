# -*- coding:utf-8 -*-
'''
Created on Jul 23, 2014

@author: andy
'''
import geometry

class Light(geometry.Ray):
    intensity = 1.0
    
    def __init__(self, org = geometry.Point(0, 0), rad = 0.0, inten = 1.0):
        geometry.Ray.__init__(self, org, rad)
        self.intensity = inten

    def incidencePoint(self, interface):
        line1 = self.toLine()
        line2 = interface.toLine()
        ipt = line1.intersectPoint(line2)
        if ipt != None and interface.hasPoint(ipt):
            return ipt
        else:
            return None

class Interface(geometry.LineSeg):
    left_refidx = 1.0
    right_refidx = 1.0
    
    def __init__(self, pt1 = geometry.Point(0,0), pt2 = geometry.Point(1,1), left_refidx = 1.0, right_refidx = 1.0):
        geometry.LineSeg.__init__(self, pt1, pt2)
        self.left_refidx = left_refidx
        self.right_refidx = right_refidx

class LightSource:
    temp = False
    __lights = []
    
    def addLight(self, light):
        self.__lights.append(light)
    
    def generateLights(self):
        return self.__lights
