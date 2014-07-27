'''
Created on Jul 27, 2014

@author: andy
'''
from optsim import *
import optdraw
import time
import math

def refracSpot((pt,rad)):
    print 'Refraction spotted'
    print "Position:%s, Light radian:%s" %(pt, rad)

if __name__ == '__main__':
    height=400
    width=400
    pt1=Point(height/2,width/2)
    pt2=Point(200,-200)
    pt3=Point(-200,-200)
    pt4=Point(-200,200)
    
    interface1=Interface(pt1,pt2)
    interface1.right_refidx=999999
    interface2 = Interface(pt2,pt3)
    interface2.right_refidx=99999
    interface3=Interface(pt3,pt4)
    interface3.right_refidx=9999
    interface4 = Interface(pt4,pt1)
    interface4.right_refidx=9999
    
    angle=20
    lt=Light(Point(0,0),math.radians(angle))
    
    sim=Simulator()
    sim.addInterface(interface1)
    sim.addInterface(interface2)    
    sim.addInterface(interface3)
    sim.addInterface(interface4)
    sim.addLight(lt)
    
    sim.addCallback('refraction', refracSpot)
    
    odraw=optdraw.OptDraw(600,600)
    
    while True:
        sim.step()
        ret=odraw.draw(sim)
        if ret=='quit':
            break
        time.sleep(0.5)