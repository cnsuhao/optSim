# -*- coding:utf-8 -*-
'''
Created on Jul 25, 2014

@author: andy
'''

from optsim import *
from math import sin, cos, tan, radians
import optdraw
import time, sys

################### 可以设置的量

# 结构参数
L0 = 800  # 水平界面的长度
L1 = 100  # 下板定长界面的长度
gap = 1  # 上下板中间间隙
pmmaidx = 1.5  # PMMA 折射率

# 界面参数，角度
# 上板
eta = 25  # (0, 90)
lamb1 = 10  # (0, 90)
# 下板
alpha = 45  # (0, 90)
# lamb2 = 20  # (0, 90)    # 没有用到

light_angles_range = range(-40, 110, 1)  # 所有光线角度
single_light_mode = False  # 是不是单光线模式，True 为单光线模式，光线依次出现，可以计算光线角度和出射位置的关系；False 为多光线模式，可以查看出光分布

####################################

# 　这些参数不要动
__quit_flag = False
__paused = False
__used_light_angles = []

def refracSpot((pt, rad)):
#     print "Refraction spotted!"
#     print "Position: %s, Light radian: %s" % (spot[0], spot[1])

    if pt.y < 0:  # 仅考虑从下表面出射的情况
        dis = pt.distanceTo(p3)
        print "Light angle: %s, distance: %s" % (__used_light_angles[0], dis)
    
        global __quit_flag
        __quit_flag = True

def simulating():
    global p1, p2, p3, p4, p5, p6
    # 计算六个点的坐标
    p1 = Point(-L0 / 2.0, 0)
    p2 = Point(L0 / 2.0, 0)
    p3 = Point(cos(radians(alpha)) * L1 - L0 / 2.0, -sin(radians(alpha)) * L1)
    p4 = Point(p1.x, p1.y + gap)
    p5 = Point(p2.x, p2.y + gap)
    a = tan(radians(lamb1)) * L0 / (tan(radians(eta)) + tan(radians(lamb1)))
    p6 = Point(a * cos(radians(eta)) - L0 / 2.0, a * sin(radians(eta)) + gap)
    
    inter1 = Interface(p1, p2)
    inter1.right_refidx = pmmaidx
    inter2 = Interface(p1, p3)
    inter2.left_refidx = pmmaidx
    inter3 = Interface(p3, p2)
    inter3.left_refidx = pmmaidx
    inter4 = Interface(p4, p5)
    inter4.left_refidx = pmmaidx
    inter5 = Interface(p4, p6)
    inter5.right_refidx = 99999
    inter6 = Interface(p6, p5)
    inter6.right_refidx = 99999  # 模拟镜面
    
    sim = Simulator()
    
    for angle in __used_light_angles:
        lt = Light(Point((p1.x + p3.x) / 2, (p1.y + p3.y) / 2), radians(angle))
        sim.addLight(lt)
    
    sim.addInterface(inter1)
    sim.addInterface(inter2)
    sim.addInterface(inter3)
    sim.addInterface(inter4)
    sim.addInterface(inter5)
    sim.addInterface(inter6)
    
    if single_light_mode:  # 单光线模式
        sim.addCallback('refraction', refracSpot)
    
    odraw = optdraw.OptDraw(L0 + 80, 400)
    
    global __quit_flag, __paused
    while not __quit_flag:
        if not __paused:
            sim.step()
        ret = odraw.draw(sim)
        if ret == 'quit':
            sys.exit()
        elif ret == 'space':
            __paused = not __paused
#         print sim
        time.sleep(0.5)
        
if __name__ == '__main__':
    if single_light_mode:
        for angle in light_angles_range:
            __quit_flag = False  # reset __quit_flag
            __used_light_angles = [angle]
            simulating()
    else:
        __used_light_angles = light_angles_range
        simulating()
