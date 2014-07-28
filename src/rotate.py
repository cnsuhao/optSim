'''
Created on Jul 24, 2014

@author: andy
'''

from optsim import *
import optdraw
import time
import math, sys

Dis = 30
Radius = 500
Max_angle = 89
Refidx = 1.5
__count = 0

def simulating(angle):
    alpha = math.radians(angle)
    pt = Point(0, 0)
    
    angle_btw = math.atan(Radius / Dis)
    
    eta1 = alpha + angle_btw
    eta2 = alpha - angle_btw
    length = math.sqrt(Dis ** 2 + Radius ** 2)
    pt1 = Point(length * math.cos(eta1), length * math.sin(eta1))
    pt2 = Point(length * math.cos(eta2), length * math.sin(eta2))
    
    interface1 = Interface(pt2, pt1)
    interface1.left_refidx = Refidx
   
    sim = Simulator()
    sim.addInterface(interface1)
    
    for angle in range(angle - Max_angle, angle + Max_angle, 1):
        lt = Light(pt, math.radians(angle))
        sim.addLight(lt)
        
    odraw = optdraw.OptDraw(Radius * 2 + 100, Radius * 2 + 100)
    global __count
    while __count <= 3:
        sim.step()
        ret = odraw.draw(sim)
        if ret == 'quit':
            sys.exit()
#         time.sleep(0.05)
        __count += 1
    
if __name__ == '__main__':
    for angle in range(0, 360 * 10, 1):
        __count = 0
        simulating(angle)
