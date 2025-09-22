#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
关卡系统模块
处理游戏关卡的加载、管理和切换
"""

class Level:
    """关卡类"""
    def __init__(self, level_number):
        """初始化关卡"""
        self.level_number = level_number
        self.width = 50
        self.height = 25
        self.ground_level = 22
        self.data = []
        self.enemies = []
        self.items = []
        self.blocks = []
        
        # 根据关卡编号加载不同内容
        if level_number == 1:
            self.load_level_1()
        else:
            self.load_default_level()
    
    def load_level_1(self):
        """加载第一关"""
        # 创建简单的地形数据
        self.data = [
            # 简单的地面
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "##################################################"
        ]
        
        # 添加一些平台
        for i in range(15, 18):
            self.data[i] = list(self.data[i])
            for j in range(10, 15):
                self.data[i][j] = '#'
            for j in range(20, 25):
                self.data[i][j] = '#'
            self.data[i] = ''.join(self.data[i])
    
    def load_default_level(self):
        """加载默认关卡"""
        # 创建简单的地形数据
        self.data = [
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "##################################################"
        ]
    
    def get_tile(self, x, y):
        """获取指定坐标的地形"""
        if 0 <= y < len(self.data) and 0 <= x < len(self.data[y]):
            return self.data[y][x]
        return ' '  # 空白区域
    
    def is_solid(self, x, y):
        """判断指定坐标是否为固体(不可穿越)"""
        tile = self.get_tile(int(x), int(y))
        return tile == '#'
    
    def get_width(self):
        """获取关卡宽度"""
        return self.width
    
    def get_height(self):
        """获取关卡高度"""
        return self.height
    
    def get_ground_level(self):
        """获取地面高度"""
        return self.ground_level