'''
Created on Jul 24, 2014

@author: andy
'''

from optsim import *
import optdraw
import time
import math

if __name__ == '__main__':
    pt = Point(0, 0)
    
    interface1 = Interface(Point(50,-400), Point(50,400))
    interface1.left_refidx = 1.5
    
    sim = Simulator()
    sim.addInterface(interface1)
    
    for angle in range(-85, 85, 1):
        lt = Light(pt, math.radians(angle))
        sim.addLight(lt)
        
    odraw = optdraw.OptDraw(600, 900)
    
    while True:
        sim.step()
        ret = odraw.draw(sim)
        if ret == 'quit':
            break
        time.sleep(0.5)
