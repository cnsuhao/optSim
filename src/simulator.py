'''
Created on Jul 23, 2014

@author: andy
'''

import geometry
import objects

class Simulator:
    def __init__(self):
        self.light_sources = list()
        self.interfaces = list()

    def addLightSource(self, ls):
        self.light_sources.append(ls)

    def addInterfaces(self, inter):
        self.interfaces.append(inter)

    def step(self):
        for ls in self.light_sources:
            lights = ls.generate()
            if isinstance(lights, list):
                for light in lights:
                    self.__trackLight(light)
            else:
                self.__trackLight(lights)

    def __trackLight(self, light):
        point_inter = dict()
        # collect all the intersect points
        for interface in self.interfaces:
            ipt = light.intersectWithLineSeg(interface)
            if ipt != None:
                point_inter[ipt] = interface

        if len(point_inter) == 0:    # no intersects at all
            return

        distances_inter = dict()
        distances = list()
        for point in point_inter:
            dis = point.distanceTo(light.origin)
            distances.append(dis)
            distances_inter[dis] = point_inter[point]

        # get the shortest
        distances.sort()
        the_point = distances[0]
        the_interface = distances_inter[the_point]

        # find if the light source is up/down the interface
        


