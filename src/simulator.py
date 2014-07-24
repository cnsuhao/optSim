# -*- coding:utf-8 -*-
'''
Created on Jul 23, 2014

@author: andy
'''

import math
import geometry
import objects

class Simulator:
    __a_light_sources = []
    __b_light_sources = []
    cur_light_sources = __a_light_sources
    next_light_sources = __b_light_sources
    interfaces = []
    
    def addLightSource(self, ls):
        self.cur_light_sources.append(ls)

    def addInterfaces(self, inter):
        self.interfaces.append(inter)

    def step(self):
        # 遍历当前所有的光源
        for ls in self.cur_light_sources:
            # 对每个光源，产生光线
            lights = ls.generateLights()
            for light in lights:
                # 处理每根光线，每根光线生成一个临时光源
                tmpls = self.__handleALight(light)
                if tmpls != None:
                    self.next_light_sources.append(tmpls)  # 加入光源列表，供下次迭代使用
            
            # 检查此光源是否临时，若否，则加入光源列表，供下次迭代继续使用
            if ls.temp != True:
                self.next_light_sources.append(ls)
        
        # 交换当前和下次的光源列表
        tmp_lss = self.next_light_sources
        self.next_light_sources = self.cur_light_sources
        self.cur_light_sources = tmp_lss
            

    def __handleALight(self, light):
        ''' 返回临时光源 '''
        # 计算光线与所有界面的入射点
        min_dis = 99999999999
        inc_point = None
        inc_interface = None
        # 取所有点中距离光线起点最近的点作为实际入射点
        for interface in self.interfaces:
            ipt = light.incidencePoint(interface)
            if ipt != None:  # 有交叉点
                # 计算到光线起点的距离
                dis = ipt.distanceTo(light.origin)
                if dis < min_dis:
                    min_dis = dis
                    inc_point = ipt
                    inc_interface = interface
        
        if inc_point == None:
            return None
        
        # 计算入射方向法线（射线）
        inter_rad = inc_interface.radian()
        candi_norm_rad = inter_rad + math.pi / 2  # 顺时针(左)旋转90度
        candi_norm_rad = geometry.regulateRadian(candi_norm_rad)
        if math.fabs(candi_norm_rad - light.radian) < math.pi / 2:
            norm_rad = candi_norm_rad
        else:
            norm_rad = geometry.regulateRadian(candi_norm_rad + math.pi)
        
        # 计算入射角
        inc_angle = math.fabs(norm_rad - light.radian)
        
        # 获得入射方向，从左往右，或从右往左
        r2l = 0
        if norm_rad == candi_norm_rad:  # 从右往左入射
            r2l = 1
        else:
            r2l = 0
            
        # 根据界面折射率参数，计算折射角
        ref_angle = 0.0
        if r2l == 1:
            ref_angle = math.asin(math.sin(inc_angle) * inc_interface.right_refidx / inc_interface.left_refidx)
        else:
            ref_angle = math.asin(math.sin(inc_angle) * inc_interface.left_refidx / inc_interface.right_refidx)
            
        # 计算临时光源的实际方向
        real_radian = 0.0
        # 检查是否全反射
        if ref_angle >= math.pi / 2:  # 全反射
            inter_angle = interface.radian()
            real_radian = light.radian + 2 * (inter_angle - light.radian)
        else:  # 折射
            if light.radian > norm_rad:
                real_radian = norm_rad + ref_angle
            else:
                real_radian = norm_rad - ref_angle
        
        real_radian = geometry.regulateRadian(real_radian)
        # 创建临时光源
        nlight = objects.Light(inc_point, real_radian)
        tls = objects.LightSource()
        tls.addLight(nlight)
        tls.temp = True
        return tls
