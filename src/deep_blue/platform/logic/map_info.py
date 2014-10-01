# -*- coding: UTF-8 -*-
# map.py
import sys
import json
from basic import *

class MapInfo(object):
    """地图"""
    def __init__(self, x_max, y_max, max_population, record_interval, time_per_round, weather):
        """Create an empty map"""
        self.types = [[0] * x_max] * y_max     ## 空地图全海洋       
        self.elements = {}
        self.max_population = max_population
        self.record_interval = record_interval
        self.time_per_round = time_per_round
        self.weather = weather

    @property
    def x_max(self):
        return len(self.types[0])

    @property
    def y_max(self):
        return len(self.types)
    
    def map_type(self, x, y): 
        """Return map type(OCEAN or LAND) on (x, y)"""
        return self.types[x][y]

    def set_map_type(self, x, y, map_type = LAND):
        """Set type on (x, y) to map_type"""
        if x >= self.x_max or y >= self.y_max:
            return False
        else:
            self.types[x][y] = LAND if map_type != OCEAN else OCEAN      # in case map_type = 2, 3, etc..
            return True

    def element(self, pos):
        """Return element at pos"""
        for element in self.elements:
            if element.pos.distance(pos) == 0:  # in case isinstance(element.pos, Rectangle), distance() is ok.
                return element
        return None

    def add_element(self, new_element):
        """Add a new element to current map"""
        for point in new_element.pos.region(level = 0, range = 0):
            if point.x >= self.x_max or point.y >= self.y_max:
                return False                    # 位置无效
            elif self.element(point) != None:
                return False                    # 位置被占用
        index = choice(xrange(10000))           # 10000以内随机生成index
        while index in self.elements.keys():    # 检查是否与已有index冲突
            index += 10000                      # 尝试解决冲突
        new_element.index = index
        self.elements[index] = new_element
        return True

    def save(self, filename):
        """Save map to file"""
        open(filename).write(saves(self))

    def saves(self):
        """Save map to string"""
        pass

    def saves_elements(self):
        """Save elements to string"""
        pass

        

def load(filename):
    """Read map from file"""
    map_str = open(filename).read()
    return loads(map_str)

def loads(map_str):
    """Read map from string"""
    parts = map_str.split('#\n')
    types = []
    for line in parts[0].split():
        types.append([int(type) for type in line])
    elements_info = parts[1].split()
    elements = []
    k = 0
    while k < len(elements_info):
        tuple = (int(elements_info[k]))
        tuple += (Position(int(elements_info[k+1]), int(elements_info[k+2]), int(elements_info[k+3])))
        tuple += (int(elements_info[k+4]))
        elements.append(tuple)
        k += 5
    return Map(types, elements)
