'''
Created on Jul 25, 2014

@author: andy
'''

from optsim import *
import time


if __name__ == '__main__':
    org = Point(0, 0)
    p1 = Point(-5, 0)
    p2 = Point(5, 0)
    p3 = Point(0, 8.66)
    
    light = Light(org, 1.047)
    lightsource = LightSource()
    lightsource.addLight(light)
    
    interface1 = Interface(p1, p2)
    interface1.right_refidx = 0.0001
    interface2 = Interface(p2, p3)
    interface2.right_refidx = 0.0001
    interface3 = Interface(p3, p1)
    interface3.right_refidx = 0.0001
    
    sim = Simulator()
    sim.addLightSource(lightsource)
    sim.addInterfaces(interface1)
    sim.addInterfaces(interface2)
    sim.addInterfaces(interface3)
    
    while True:
        sim.step()
        print sim
        time.sleep(1)