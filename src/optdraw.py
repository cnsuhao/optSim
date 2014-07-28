# -*- coding:utf-8 -*-
'''
Created on Jul 26, 2014

@author: andy
'''

import pygame
from pygame.locals import *

class OptDraw(object):
    '''
    classdocs
    '''

    def __init__(self, w=640, h=480):
        '''
        Constructor
        '''
        pygame.init()
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption("OptDraw")
        
        self.light_color = (255, 255, 150)
        self.interface_color = (100, 100, 150)
        
    def __draw_axis__(self):
        pass
    
    def draw(self, simulator):
        self.screen.fill((0, 0, 0))
        lights = simulator.getLights()
        for light in lights:
            self.__drawLight(light)
        
        interfaces = simulator.getInterfaces()
        for inter in interfaces:
            self.__drawInterface(inter)
            
        pygame.display.update()
        
        # 返回键盘、鼠标事件
        for event in pygame.event.get():
            if (event.type == QUIT):
                return 'quit'
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 'esc'
                elif event.key == K_SPACE:
                    return 'space'
                else:
                    return None
        
    def __drawLight(self, light):
        if light.hitpoint != None:
            pygame.draw.line(self.screen, self.light_color, self.__traslate(light.origin.toTuple()), self.__traslate(light.hitpoint.toTuple()), int(light.intensity))
        else:
            line = light.toLine()
            p2_x = (line.point2.x - line.point1.x) * 100 + line.point1.x     # 直线原长是1，延长100倍
            p2_y = (line.point2.y - line.point1.y) * 100 + line.point1.y
            pygame.draw.line(self.screen, self.light_color, self.__traslate(line.point1.toTuple()), self.__traslate((p2_x, p2_y)), int(light.intensity))
            
    def __drawInterface(self, inter):
        pygame.draw.line(self.screen, self.interface_color, self.__traslate(inter.start.toTuple()), self.__traslate(inter.end.toTuple()), 2)
        
        
    def __traslate(self, real_pos):
        return (self.width / 2.0 + real_pos[0], self.height / 2.0 - real_pos[1])
        
