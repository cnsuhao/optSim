# -*- coding:utf-8 -*-
'''
Created on Jul 25, 2014

@author: andy
'''

from optsim import *
import time, sys
import matplotlib.pyplot as plt
from math import sin, cos, tan, radians

######################################################################## 可以设置的量

# 结构参数，填写实际长度，单位随意选择，统一即可
L0 = 100  # 水平界面的长度
L1 = 15  # 下板定长界面的长度
source_number = 100  # 定长界面上放置多少个光源
angle_range = 30  # 每个光源的光线与法线的夹角范围（角度）
gap = 1  # 上下板中间间隙
pmmaidx = 1.5  # PMMA 折射率
statistics_div = 100  # 统计时下板被分成多少份

# 界面参数，角度
# 上板
H1_range = (x / 10.0 for x in xrange(10, 100, 1))  # H1长度变化范围：1~10, 增长０.1
eta_range = xrange(30, 70, 5)  # eta角度变化范围
lamb1_range = xrange(30, 70, 5)  # lamb1角度变化范围
# 下板
H2_range = (x / 10.0 for x in xrange(10, 100, 1))  # H2长度变化范围：1~10, 增长０.1
alpha_range = xrange(30, 70, 5)  # alpha角度变化范围
# lamb2 # 没有用到

# 程序控制相关参数
enable_canvas = True  # 是否显示光线图
enable_plot = True  # 是否绘制统计图（绘制统计图时需要手动关闭绘图窗口才能继续下个计算）

########################################################################

# 运行时参数，不要改
# 为了显示美观作些缩放，缩放不会影响光路
__scaled_ratio = 800.0 / L0  # 缩放比率
__scaled_L0 = L0 * __scaled_ratio
__scaled_L1 = L1 * __scaled_ratio
__scaled_gap = gap * __scaled_ratio 
__scaled_H1_range = (x * __scaled_ratio for x in H1_range)  # H1长度变化范围
__scaled_H2_range = (x * __scaled_ratio for x in H2_range)  # H2长度变化范围

__quit = False
__paused = False
__distance_set = set()
__down_interface = None
__statistics_length = 0.0

#===================================

def refracSpot(light):
    global  __distance_set, __down_interface
    
    if __down_interface.hasPoint(light.origin):  # 出射点在下底板上
        dis = light.origin.distanceTo(__down_interface.start)
        __distance_set.add(dis)

def calStatistics(vals):
    sum1 = 0
    sum2 = 0
    for v in vals:
        sum1 += v
        sum2 += v ** 2    
    mean = 1.0 * sum1 / len(vals)
    var = 1.0 * sum2 / len(vals) - mean ** 2
    return (sum1, mean, var)

def simulating(cur_alpha, cur_H2, cur_eta, cur_H1, cur_lamb1):
    global __statistics_length, __down_interface, __distance_set
    # 计算六个点的坐标
    p1 = Point(-__scaled_L0 / 2.0, 0)
    p2 = Point(__scaled_L0 / 2.0, 0)
    p3 = Point(cos(radians(cur_alpha)) * __scaled_L1 - __scaled_L0 / 2.0, -sin(radians(cur_alpha)) * __scaled_L1)
    p4 = Point(p1.x, p1.y + __scaled_gap)
    p5 = Point(p2.x, p2.y + __scaled_gap)
    a = tan(radians(cur_lamb1)) * (__scaled_L0 + cur_H1 / tan(radians(cur_lamb1))) / (tan(radians(cur_eta)) + tan(radians(cur_lamb1)))
    p6 = Point(a * cos(radians(cur_eta)) - __scaled_L0 / 2.0, a * sin(radians(cur_eta)) + __scaled_gap)
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
    inter5.right_refidx = 9999999
    inter6 = Interface(p6, p8)
    inter6.right_refidx = 9999999  # 模拟镜面
    inter8 = Interface(p8, p5)
    inter8.right_refidx = 9999999
    
    __down_interface = inter3  # 三号板是下底板
    __statistics_length = __down_interface.length() / statistics_div
    
    sim = Simulator()
    
    light_angles_range = xrange(90 - cur_alpha - angle_range, 90 - cur_alpha + angle_range + 1, 1)  # 所有光线角度
    for part in xrange(1, source_number + 1):
        pos_x = (p3.x - p1.x) / (source_number + 1) * part + p1.x 
        pos_y = (p3.y - p1.y) / (source_number + 1) * part + p1.y
        for angle in light_angles_range:
            lt = Light(Point(pos_x, pos_y), radians(angle))
            lt.transient = True  # 设置为瞬时光源加快计算速度，且容易判断结束
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
    
    if enable_canvas:
        canvas = Canvas(__scaled_L0 + 100, max(p6.y, -p3.y) * 2 + 50, False)
        
    global __quit, __paused
    while not __quit:
        if not __paused:
            sim.step()
            
        # 是否绘制光线图
        if enable_canvas:
            ret = canvas.draw(sim)
            if ret == 'quit':
                sys.exit()
            elif ret == 'space':
                __paused = not __paused

        # 判断模拟是否结束，统计数据
        if len(sim.getLights()) == 0:  # 没有光线了就是模拟结束
            # 统计出射点数
            statistics_result = {}
            for part in xrange(0, statistics_div):
                runCount = 0
                dis_start = part * __statistics_length
                dis_end = dis_start + __statistics_length
                for dis in __distance_set:
                    if dis_start <= dis < dis_end:
                        runCount += 1
                statistics_result[part] = runCount
            # 求统计属性
            (total, mean, variance) = calStatistics(statistics_result.values())
    #                 print "<<< Hist: %s" % statistics_result.values()
            print "%.1f\t%.1f\t%s\t" % (mean, variance, total),
            sys.stdout.flush()
            
            # 画柱状图
            if enable_plot:
                index = xrange(0, statistics_div)
                plt.bar(index, statistics_result.values(), 1, alpha=0.6)
                plt.xlabel('Distance')
                plt.ylabel('Light Counts')
                plt.title('Distribution of lights emiting from the lower interface')
                plt.show()
            
            # 重置数据，退出这次模拟
            __distance_set.clear()
            __quit = True
        
if __name__ == '__main__':
    print "Num\tAlpha\tH2\tEta\tH1\tLamb1\tMean\tVar\tTotal\tET(sec)]"
    runCount = 0
    # 遍历全部配置
    for alph in alpha_range:
        for h2 in __scaled_H2_range:
            for et in eta_range:
                for h1 in __scaled_H1_range:
                    for lam1 in lamb1_range:
                        print "%s\t%s\t%s\t%s\t%s\t%s\t" % (runCount, alph, h2 / __scaled_ratio, et, h1 / __scaled_ratio, lam1),
                        sys.stdout.flush()
                        __quit = False
                        start = time.time()
                        simulating(alph, h2, et, h1, lam1)
                        print "%.2f" % (time.time() - start)
                        runCount += 1
