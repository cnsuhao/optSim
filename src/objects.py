# -*- coding:utf-8 -*-
'''
Created on Jul 23, 2014

@author: andy
'''
import geometry

class Light(geometry.Ray):
    def __init__(self, org=geometry.Point(0, 0), rad=0.0, inten=1.0):
        geometry.Ray.__init__(self, org, rad)
        self.intensity = inten

    def incidencePoint(self, interface):
        line1 = self.toLine()
        line2 = interface.toLine()
        ipt = line1.intersectPoint(line2)
        if (ipt != None) and (ipt != self.origin) and (interface.hasPoint(ipt)):
            return ipt
        else:
            return None
        
    def __str__(self):
        string = "Light: %s [%s] --> (%s)" %(self.origin, self.intensity, self.radian)
        return string

    def __repr__(self):
        string = "Light: %s [%s] --> (%s)" %(self.origin, self.intensity, self.radian)
        return string

class Interface(geometry.LineSeg):
    def __init__(self, pt1=geometry.Point(0, 0), pt2=geometry.Point(1, 1), left_refidx=1.0, right_refidx=1.0):
        geometry.LineSeg.__init__(self, pt1, pt2)
        self.left_refidx = left_refidx
        self.right_refidx = right_refidx
        
    def __str__(self):
        string = "Interface: (%s) %s -- %s (%s)" %(self.left_refidx, self.start, self.end, self.right_refidx)
        return string
    
    def __repr__(self):
        string = "Interface: (%s) %s -- %s (%s)" %(self.left_refidx, self.start, self.end, self.right_refidx)
        return string

class LightSource:
    def __init__(self):
        self.temp = False
        self.__lights = []
    
    def addLight(self, light):
        self.__lights.append(light)
    
    def generateLights(self):
        return self.__lights
    
    def __str__(self):
        string = "Light Source: "
        for light in self.__lights:
            string += "  %s" %light
        
        return string

    def __repr__(self):
        string = "Light Source: "
        for light in self.__lights:
            string += "   %s" %light
        
        return string
