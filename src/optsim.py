# -*- coding:utf-8 -*-
'''
Created on Jul 25, 2014

@author: andy
'''

import math

###################### Geometry

def equal(v1, v2):
    epsilon = 0.000001
    return math.fabs(v1 - v2) <= epsilon

def regulateRadian(rad):
    r = rad
    while not (r >= 0 and r < math.pi * 2):
        if r < 0:
            r += math.pi * 2
        else:
            r -= math.pi * 2
    return r

class Point:
    def __init__(self, xpos=0.0, ypos=0.0):
        self.x = xpos * 1.0  # to float
        self.y = ypos * 1.0

    def shift(self, vec):
        return Point(self.x + vec.u, self.y + vec.v)

    def distanceTo(self, pt):
        return math.sqrt((pt.x - self.x) ** 2 + (pt.y - self.y) ** 2)

    def __eq__(self, pt):
        if not isinstance(pt, Point):
            return False
        else:
            return equal(self.distanceTo(pt), 0.0)
        
    def __ne__(self, pt):
        return not self.__eq__(pt)
        
    def __str__(self):
        string = "<%s, %s>" % (self.x, self.y) 
        return string

    def __repr__(self):
        string = "<%s, %s>" % (self.x, self.y) 
        return string

class Ray:
    def __init__(self, org=Point(0, 0), rad=0.0):
        self.origin = org
        self.radian = regulateRadian(rad)  # 转换到[0, 360)

    def toLine(self):
        end_point = Point(self.origin.x + math.cos(self.radian), self.origin.y + math.sin(self.radian))
        return Line(self.origin, end_point)

    def __eq__(self, other):
        if not isinstance(other, Ray):
            return False
        else:
            return self.origin == other.origin and equal(self.radian, other.radian)
        
    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        string = "%s --> (%s)" % (self.origin, self.radian)
        return string
    
    def __repr__(self):
        string = "%s --> (%s)" % (self.origin, self.radian)
        return string

class Line:
    def __init__(self, pt1=Point(0, 0), pt2=Point(1, 1)):
        if pt1 == pt2:
            raise ArithmeticError, "invalid Line: %s" % self
        else:
            self.point1 = pt1
            self.point2 = pt2

    def intersectPoint(self, line):
        a = self.point1
        b = self.point2
        c = line.point1
        d = line.point2

        if equal(self.slope(), line.slope()):
            print "The two lines are parrelled!"
            return None
        else:
            ipt = Point()
            ipt.x = ((b.x - a.x) * (c.x - d.x) * (c.y - a.y) - c.x * (b.x - a.x) * (c.y - d.y) + a.x * (b.y - a.y) * (c.x - d.x)) / ((b.y - a.y) * (c.x - d.x) - (b.x - a.x) * (c.y - d.y))
            ipt.y = ((b.y - a.y) * (c.y - d.y) * (c.x - a.x) - c.y * (b.y - a.y) * (c.x - d.x) + a.y * (b.x - a.x) * (c.y - d.y)) / ((b.x - a.x) * (c.y - d.y) - (b.y - a.y) * (c.x - d.x))
            return ipt

    def slope(self):
        if equal(self.point2.x, self.point1.x):
            return float('inf')
        else:
            return (self.point2.y - self.point1.y) / (self.point2.x - self.point1.x)

    def parallelWith(self, line):
        return equal(self.slope(), line.slope())

    def __str__(self):
        string = "-- %s -- %s --" % (self.point1, self.point2)
        return string

    def __repr__(self):
        string = "-- %s -- %s --" % (self.point1, self.point2)
        return string


class LineSeg:
    def __init__(self, pt1=Point(0, 0), pt2=Point(1, 1)):
        if pt1 == pt2:
            raise ArithmeticError, "invalid LineSeg: %s" % self
        else:
            self.start = pt1
            self.end = pt2

    def length(self):
        return math.sqrt((self.end.x - self.start.x) ** 2 + (self.end.y - self.start.y) ** 2)
    
    def radian(self):
        delta_x = self.end.x - self.start.x
        delta_y = self.end.y - self.start.y
        if delta_x == 0:
            if delta_y > 0:
                return math.pi / 2
            elif delta_y < 0:
                return math.pi * 3 / 4
            else:
                raise ArithmeticError, "invalid LineSeg: %s" % self
        
        rad = math.atan(math.fabs(delta_y / delta_x))
        if delta_x > 0 and delta_y > 0:  # first quadrant
            return rad
        elif delta_x < 0 and delta_y > 0:  # second quadrant
            return math.pi - rad
        elif delta_x < 0 and delta_y < 0:  # third quadrant
            return math.pi + rad
        else:  # forth quadrant
            return 2 * math.pi - rad

    def hasPoint(self, pt):
        ac = self.length()
        ab = self.start.distanceTo(pt)
        bc = pt.distanceTo(self.end)
        if equal(ac, (ab + bc)):
            return True
        else:
            return False

    def toLine(self):
        return Line(self.start, self.end)

    def __str__(self):
        string = "%s -- %s" % (self.start, self.end)
        return string

    def __repr__(self):
        string = "%s -- %s" % (self.start, self.end)
        return string

######################## Objects 

class Light(Ray):
    def __init__(self, org=Point(0, 0), rad=0.0, inten=1.0):
        Ray.__init__(self, org, rad)
        self.intensity = inten

    def incidencePoint(self, interface):
        line1 = self.toLine()
        line2 = interface.toLine()
        ipt = line1.intersectPoint(line2)
        if (ipt != None) and (ipt != self.origin):  # 交点需存在且不是光线起点
            linesg = LineSeg(self.origin, ipt)
            # 在光线方向上， 在界面上 
            if equal(linesg.radian(), self.radian) and interface.hasPoint(ipt):
                return ipt
            else:
                return None
        else:
            return None
        
    def __str__(self):
        string = "Light: %s [%s] --> (%s)" % (self.origin, self.intensity, self.radian)
        return string

    def __repr__(self):
        string = "Light: %s [%s] --> (%s)" % (self.origin, self.intensity, self.radian)
        return string

class Interface(LineSeg):
    def __init__(self, pt1=Point(0, 0), pt2=Point(1, 1), left_refidx=1.0, right_refidx=1.0):
        LineSeg.__init__(self, pt1, pt2)
        self.left_refidx = left_refidx * 1.0
        self.right_refidx = right_refidx * 1.0
        
    def __str__(self):
        string = "Interface: (%s) %s -- %s (%s)" % (self.left_refidx, self.start, self.end, self.right_refidx)
        return string
    
    def __repr__(self):
        string = "Interface: (%s) %s -- %s (%s)" % (self.left_refidx, self.start, self.end, self.right_refidx)
        return string

class LightSource:
    def __init__(self):
        self.temp = False
        self.__lights = []
    
    def addLight(self, light):
        self.__lights.append(light)
    
    def generateLights(self):
        return self.__lights
    
    def __str__(self):
        string = "Light Source: "
        for light in self.__lights:
            string += "  %s" % light
        
        return string

    def __repr__(self):
        string = "Light Source: "
        for light in self.__lights:
            string += "   %s" % light
        
        return string
    
####################### The simulator
    
class Simulator:
    def __init__(self):
        self.__a_light_sources = []
        self.__b_light_sources = []
        self.cur_light_sources = self.__a_light_sources
        self.next_light_sources = self.__b_light_sources
        self.interfaces = []
        self.step_count = 0
    
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
        
        # 轮转当前光源列表
        tmp_lss = self.cur_light_sources
        self.cur_light_sources = self.next_light_sources
        self.next_light_sources = tmp_lss
        # 清空下次光源列表
        while len(self.next_light_sources) > 0:
            self.next_light_sources.pop()
        
        self.step_count += 1
            

    def __handleALight(self, light):
        ''' 返回临时光源 '''
        # 计算光线与所有界面的入射点
        min_dis = float('inf')
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
        r2l = 0     # 入射方向，从右向左？
        inter_rad = inc_interface.radian()
        candi_norm_rad = inter_rad + math.pi / 2  # 逆时针(左)旋转90度
        candi_norm_rad = regulateRadian(candi_norm_rad)  # 转换到[0,360)
        if math.fabs(candi_norm_rad - light.radian) < math.pi / 2:
            norm_rad = candi_norm_rad
            r2l = 1     # 从右向左
        else:
            norm_rad = regulateRadian(candi_norm_rad + math.pi)
            r2l = 0     # 从左向右
        
        # 计算入射角
        inc_angle = math.fabs(norm_rad - light.radian)
            
        # 根据界面折射率参数，计算折射或反射光线角度
        in_refix = 0.0
        out_refix = 0.0
        if r2l == 1:
            in_refix = inc_interface.right_refidx
            out_refix = inc_interface.left_refidx
        else:  # 从左往右入射
            in_refix = inc_interface.left_refidx
            out_refix = inc_interface.right_refidx
            
        # 检查是否达到临界角
        result_radian = 0.0
        critical_angle = math.asin(out_refix / in_refix)
        if inc_angle >= critical_angle:  # 全反射， 计算反射角
            inter_angle = inc_interface.radian()
            result_radian = light.radian + 2 * (inter_angle - light.radian)
        else:  # 折射，计算折射角
            ref_angle = math.asin(math.sin(inc_angle) * in_refix / out_refix)
            if light.radian > norm_rad:
                result_radian = norm_rad + ref_angle
            else:
                result_radian = norm_rad - ref_angle

        result_radian = regulateRadian(result_radian)
        # 创建临时光源
        nlight = Light(inc_point, result_radian)
        tls = LightSource()
        tls.addLight(nlight)
        tls.temp = True
        return tls
    
    def __str__(self):
        string = "------------------ Step: %s ------------------ \n" % self.step_count
        for ls in self.cur_light_sources:
            string += "%s\n" % ls
        
        for inter in self.interfaces:
            string += "%s\n" % inter
        
        return string

    def __repr__(self):
        string = "------------------ Step: %s ------------------ \n" % self.step_count
        for ls in self.cur_light_sources:
            string += "%s\n" % ls
        
        for inter in self.interfaces:
            string += "%s\n" % inter
        
        return string
