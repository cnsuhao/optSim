# -*- coding:utf-8 -*-
from optsim import *
import matplotlib.pyplot as plt
import math, sys

L = 120  # 光导长度
H = 100  # 两版间距
pmmaidx = 1.5
sourceNum = 10  # 放置的光源个数
angleRange = 42  # 每个光源光线的角度范围: -42~42
statDiv = 120  # 统计区域个数

__upInterface = None
__distanceIntensityDict = {}
__quit = False

def reflecSpot(light):
    global __distanceIntensityDict, __upInterface, __quit
    
    if __upInterface.hasPoint(light.origin):
        dis = light.origin.distanceTo(__upInterface.end)
        
        inten = light.intensity
        
        if __distanceIntensityDict.has_key(dis):
            __distanceIntensityDict[dis] += inten
        else:
            __distanceIntensityDict[dis] = inten

if __name__ == '__main__':
    p1 = Point(-L / 2.0, 0)
    p2 = Point(L / 2.0, 0)
    p3 = Point(L / 2.0, H)
    p4 = Point(-L / 2.0, H)
    inter1 = Interface(p1, p2)
    inter1.left_refidx = pmmaidx
    inter2 = Interface(p3, p4)
    inter2.left_refidx = pmmaidx
    
    __upInterface = inter2
    
    sim = Simulator()
    sim.addInterface(inter1)
    sim.addInterface(inter2)
    
    for index in xrange(1, sourceNum + 1, 1):
        source_x = -L / 2.0
        source_y = H / (sourceNum + 1) * index
        
        light_angles_range_10x = xrange(-angleRange * 10 , angleRange * 10, 1)
        for angle10x in light_angles_range_10x:
            angle = angle10x / 10.0
            lt = Light(Point(source_x, source_y), math.radians(angle))
            lt.intensity = math.cos(math.radians(angle))  # 强度满足高斯分布
            lt.transient = True
            sim.addLight(lt)
    
    sim.addCallback("reflection", reflecSpot)  # 添加全反射的回调函数

    canvas = Canvas(800, 600, False)
    
    runCount = 0
    while not __quit:
        sim.step()
        ret = canvas.draw(sim)
        if ret == 'quit':
            sys.exit()
        
        if runCount > 100:  # 运行一百次，模拟结束，开始统计
            stat_result = []
            for index in xrange(0, statDiv):
                dis_start = index * 1.0 * L / statDiv
                dis_end = dis_start + 1.0 * L / statDiv
                
                intensity = 0
                for dis, inten in __distanceIntensityDict.items():
                    if dis > dis_start and dis < dis_end:
                        intensity += inten
                
                stat_result.append(intensity)
                
            print stat_result  # 打印距离列表
            
            # 画柱状图
            index = xrange(0, statDiv)
            plt.bar(index, stat_result, 1, alpha=0.6)
            plt.xlabel('Distance')
            plt.ylabel('Intensity')
            plt.title('Distribution of Light Intensity')
            plt.show()
            
            __quit = True  # 退出程序
            raw_input("按回车键退出")

        runCount += 1
            
        
    
    
