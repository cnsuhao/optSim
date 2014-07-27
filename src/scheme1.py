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
Division = 100  # 分成一百分，放置光源
H1 = 10  # 　上挡板高度
H2 = 10  # 下挡板高度
gap = 1  # 上下板中间间隙
pmmaidx = 1.5  # PMMA 折射率

# 界面参数，角度
# 上板
eta = 50  # (0, 90)
lamb1 = 10  # (0, 90)
# 下板
alpha = 45  # (0, 90)
# lamb2 = 20  # (0, 90)    # 没有用到

light_angles_range = range(90 - alpha - 30, 90 - alpha + 30, 1)  # 所有光线角度
single_light_mode = False  # 是不是单光线模式，True 为单光线模式，光线依次出现，可以计算光线角度和出射位置的关系；False 为多光线模式，可以查看出光分布
statistics_div = 100

####################################

# 　这些参数不要动
__quit_flag = False
__paused = False
__used_light_angles = []
__distance_set = set()
__down_inter_length = 0.0 
__statistics_length = 0.0

def refracSpot((pt, rad)):
    global __quit_flag, __distance_set
    
    if pt.y < 0:  # 仅考虑从下表面出射的情况
        dis = pt.distanceTo(p3)
        
        if single_light_mode:
            print "Light angle: %s, distance: %s" % (__used_light_angles[0], dis)
            __quit_flag = True
        else:
            total_points = len(light_angles_range) * (Division - 1)
            __distance_set.add(dis)
            print "%s/%s" % (len(__distance_set), total_points)
            
            if len(__distance_set) == total_points:
                print "Stage completed, do the analysis..."
                # 统计出射点数
                statistics_result = {}
                for part in range(0, statistics_div):
                    count = 0
                    dis_start = part * __statistics_length
                    dis_end = (part + 1) * __statistics_length
                    for dis in __distance_set:
                        if dis >= dis_start and dis < dis_end:
                            count += 1
                    statistics_result[part] = count
                # 求方差
                variance = calVariance(statistics_result.values())
                print statistics_result.values
                print "*** Variance is %s" % variance
                
                print "Done, Next stage..."
                # FIXME clear set!
                __quit_flag = True
            

def calVariance(vals):
    sum1 = 0.0
    sum2 = 0.0
    for v in vals:
        sum1 += v
        sum2 += v ** 2 
    
    mean = sum1 / len(vals)
    var = sum2 / len(vals) - mean ** 2
    return var

def simulating():
    global p1, p2, p3, p4, p5, p6, __down_inter_length, __statistics_length
    # 计算六个点的坐标
    p1 = Point(-L0 / 2.0, 0)
    p2 = Point(L0 / 2.0, 0)
    p3 = Point(cos(radians(alpha)) * L1 - L0 / 2.0, -sin(radians(alpha)) * L1)
    p4 = Point(p1.x, p1.y + gap)
    p5 = Point(p2.x, p2.y + gap)
    a = tan(radians(lamb1)) * (L0 + H1 / tan(radians(lamb1))) / (tan(radians(eta)) + tan(radians(lamb1)))
    p6 = Point(a * cos(radians(eta)) - L0 / 2.0, a * sin(radians(eta)) + gap)
    # 新加的右侧挡板上两点
    p7 = Point(p2.x, p2.y - H2)
    p8 = Point(p5.x, p5.y + H1)
    __down_inter_length = p7.distanceTo(p3)  # 保存下界面的长度
    __statistics_length = __down_inter_length / statistics_div
    
    inter1 = Interface(p1, p2)
    inter1.right_refidx = pmmaidx
    inter2 = Interface(p1, p3)
    inter2.left_refidx = pmmaidx
    inter3 = Interface(p3, p7)
    inter3.left_refidx = pmmaidx
    inter7 = Interface(p7, p2)
    inter7.left_refidx = pmmaidx
    inter4 = Interface(p4, p5)
    inter4.left_refidx = pmmaidx
    inter5 = Interface(p4, p6)
    inter5.right_refidx = 9999
    inter6 = Interface(p6, p8)
    inter6.right_refidx = 9999  # 模拟镜面
    inter8 = Interface(p8, p5)
    inter8.right_refidx = 9999
    
    sim = Simulator()
    
    for part in range(1, Division):
        pos_x = (p3.x - p1.x) / Division * part + p1.x 
        pos_y = (p3.y - p1.y) / Division * part + p1.y
        for angle in __used_light_angles:
            lt = Light(Point(pos_x, pos_y), radians(angle))
            sim.addLight(lt)
    
    sim.addInterface(inter1)
    sim.addInterface(inter2)
    sim.addInterface(inter3)
    sim.addInterface(inter4)
    sim.addInterface(inter5)
    sim.addInterface(inter6)
    sim.addInterface(inter7)
    sim.addInterface(inter8)
    
    sim.addCallback('refraction', refracSpot)
    
    odraw = optdraw.OptDraw(L0 + 100, 400)
    
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
#         time.sleep(0.1)
        
if __name__ == '__main__':
    if single_light_mode:
        for angle in light_angles_range:
            __quit_flag = False  # reset __quit_flag
            __used_light_angles = [angle]
            simulating()
    else:
        __used_light_angles = light_angles_range
        simulating()
