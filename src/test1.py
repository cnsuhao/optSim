'''
Created on Jul 24, 2014

@author: andy
'''

from optsim import *

if __name__ == '__main__':
    origin = Point(0, 0)
    hori_light1 = Light(origin, 0)
    ls = LightSource()
    ls.addLight(hori_light1)
    interface1 = Interface(Point(1,0), Point(0,1))
    sim = Simulator()
    sim.addLightSource(ls)
    sim.addInterfaces(interface1)
    while True:
        sim.step()
