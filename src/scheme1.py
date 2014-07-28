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
Division = 50  # 分成一百分，放置光源
H1 = 10  # 　上挡板高度
H1_range = range(1, 10, 2)
H2 = 10  # 下挡板高度
H2_range = range(1, 10, 2)
gap = 1  # 上下板中间间隙
pmmaidx = 1  # PMMA 折射率

# 界面参数，角度
# 上板
eta_range = range(20, 70, 5)
lamb1_range = range(20, 70, 5)
# 下板
alpha_range = range(20, 70, 5)
# lamb2 # 没有用到

light_angle_start = -30     # 光线相对于法线的起始角度（包括）
light_angle_end = 30    # 光线的终止角度（包括）

statistics_div = 100

####################################

# 　这些参数不要动
__next_config = False
__paused = False
__detected_out_lights = set()
__distance_set = set()
__up_gap_interface = None
__down_gap_interface = None
__down_interface = None

def refracSpot(light):
    global __next_config, __distance_set, __detected_out_lights, __down_interface
    
    if not (light.origin.y == 0 or light.origin.y == gap):  # 排除间隙之间的折射
        if not __next_config:
            total_points = (light_angle_end - light_angle_start + 1) * (Division - 1)
            __detected_out_lights.add(light)
            print "%s/%s\r" % (len(__detected_out_lights), total_points)
            
            if __down_interface.hasPoint(light.origin):  # 出射点在下底板上
                dis = light.origin.distanceTo(p3)
                __distance_set.add(dis)
        
            if len(__detected_out_lights) == total_points:  # 检测到所有光线都已出射，开始统计分析
#                     print "Stage completed, do the analysis..."
                # 统计出射点数
                statistics_result = {}
                statistics_length = __down_interface.length() / statistics_div
                for part in range(0, statistics_div):
                    count = 0
                    dis_start = part * statistics_length
                    dis_end = (part + 1) * statistics_length
                    for dis in __distance_set:
                        if dis >= dis_start and dis < dis_end:
                            count += 1
                    statistics_result[part] = count
                # 求统计属性
                (total, mean, variance) = calStatistics(statistics_result.values())
                print "Hist: %s" % statistics_result.values()
                print "Total: %s, Mean: %s, Variance: %s" % (total, mean, variance)
                
                # cleanup
                __detected_out_lights.clear()
                __distance_set.clear()
            
#                     print "Done, Next Config..."
                print "-------------------------------------------------------------------------"
                __next_config = True

def calStatistics(vals):
    sum1 = 0.0
    sum2 = 0.0
    for v in vals:
        sum1 += v
        sum2 += v ** 2    
    mean = sum1 / len(vals)
    var = sum2 / len(vals) - mean ** 2
    return (sum1, mean, var)

def simulating(cur_alpha, cur_H2, cur_eta, cur_H1, cur_lamb1):
    global p1, p2, p3, p4, p5, p6, __statistics_length, __down_interface, __up_gap_interface, __down_gap_interface
    print "Current Simulating [alpha: %s, H2: %s, eta: %s, H1: %s, lamb1: %s]" % (cur_alpha, cur_H2, cur_eta, cur_H1, cur_lamb1)
    # 计算六个点的坐标
    p1 = Point(-L0 / 2.0, 0)
    p2 = Point(L0 / 2.0, 0)
    p3 = Point(cos(radians(cur_alpha)) * L1 - L0 / 2.0, -sin(radians(cur_alpha)) * L1)
    p4 = Point(p1.x, p1.y + gap)
    p5 = Point(p2.x, p2.y + gap)
    a = tan(radians(cur_lamb1)) * (L0 + cur_H1 / tan(radians(cur_lamb1))) / (tan(radians(cur_eta)) + tan(radians(cur_lamb1)))
    p6 = Point(a * cos(radians(cur_eta)) - L0 / 2.0, a * sin(radians(cur_eta)) + gap)
    # 新加的右侧挡板上两点
    p7 = Point(p2.x, p2.y - cur_H2)
    p8 = Point(p5.x, p5.y + cur_H1)
    
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
    # 间隙两端挡板
    inter9 = Interface(p4, p1)
    inter10 = Interface(p5, p2)
    
    __up_gap_interface = inter4  # 上间隙板
    __down_gap_interface = inter1  # 下间隙板
    __down_interface = inter3  # 三号板是下底板
    
    sim = Simulator()
    
    light_angles_range = range(90 - cur_alpha + light_angle_start, 90 - cur_alpha + light_angle_end + 1, 1)  # 所有光线角度
    for part in range(1, Division):
        pos_x = (p3.x - p1.x) / Division * part + p1.x 
        pos_y = (p3.y - p1.y) / Division * part + p1.y
        for angle in light_angles_range:
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
    sim.addInterface(inter9)
    sim.addInterface(inter10)
    
    sim.addCallback('refraction', refracSpot)
    
    odraw = optdraw.OptDraw(L0 + 100, 400)
    
    global __next_config, __paused
    while not __next_config:
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
    # 全部配置
    for alph in alpha_range:
        for h2 in H2_range:
            for et in eta_range:
                for h1 in H1_range:
                    for lam1 in lamb1_range:
                        __next_config = False
                        simulating(alph, h2, et, h1, lam1)
