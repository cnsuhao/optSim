'''
Created on Jul 25, 2014

@author: andy
'''

from optsim import *
import optdraw
import time


if __name__ == '__main__':
    org = Point(0, 0)
    p1 = Point(-50, 0)
    p2 = Point(50, 0)
    p3 = Point(0, 87)
    
    light = Light(org, 1.047)
    
    interface1 = Interface(p1, p2)
    interface1.right_refidx = 0.0001
    interface2 = Interface(p2, p3)
    interface2.right_refidx = 0.0001
    interface3 = Interface(p3, p1)
    interface3.right_refidx = 0.0001
    
    sim = Simulator()
    sim.addLight(light)
    sim.addInterface(interface1)
    sim.addInterface(interface2)
    sim.addInterface(interface3)
    
    odraw = optdraw.OptDraw(200, 200)
    while True:
        sim.step()
#         print sim
        odraw.draw(sim)
        time.sleep(1)