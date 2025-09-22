#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
物理引擎模块
处理游戏中的物理效果，如重力、碰撞等
"""

class PhysicsEngine:
    """物理引擎"""
    def __init__(self):
        """初始化物理参数"""
        self.gravity = 0.5
        self.terminal_velocity = 10
    
    def apply_gravity(self, obj):
        """对对象应用重力"""
        if not hasattr(obj, 'on_ground') or not obj.on_ground:
            obj.vy += self.gravity
            # 限制最大下落速度
            if obj.vy > self.terminal_velocity:
                obj.vy = self.terminal_velocity
    
    def check_ground_collision(self, obj, ground_level):
        """检查与地面的碰撞"""
        # 简单的地面碰撞检测
        if obj.y + obj.height >= ground_level:
            obj.y = ground_level - obj.height
            obj.vy = 0
            if hasattr(obj, 'on_ground'):
                obj.on_ground = True
                if hasattr(obj, 'jumping'):
                    obj.jumping = False
    
    def check_wall_collision(self, obj, left_wall, right_wall):
        """检查与墙壁的碰撞"""
        # 左墙碰撞
        if obj.x <= left_wall:
            obj.x = left_wall
            obj.vx = 0
        
        # 右墙碰撞
        if obj.x + obj.width >= right_wall:
            obj.x = right_wall - obj.width
            obj.vx = 0
    
    def resolve_collision(self, obj1, obj2):
        """解决两个对象之间的碰撞"""
        # 简单的碰撞反应
        # 计算重叠量
        overlap_x = min(obj1.x + obj1.width - obj2.x, obj2.x + obj2.width - obj1.x)
        overlap_y = min(obj1.y + obj1.height - obj2.y, obj2.y + obj2.height - obj1.y)
        
        # 分离对象
        if overlap_x < overlap_y:
            # 水平分离
            if obj1.x < obj2.x:
                obj1.x -= overlap_x / 2
                obj2.x += overlap_x / 2
            else:
                obj1.x += overlap_x / 2
                obj2.x -= overlap_x / 2
            
            # 反弹效果
            obj1.vx *= -0.5
            obj2.vx *= -0.5
        else:
            # 垂直分离
            if obj1.y < obj2.y:
                obj1.y -= overlap_y / 2
                obj2.y += overlap_y / 2
                # 如果是下落碰撞，停止垂直速度
                if obj1.vy > 0:
                    obj1.vy = 0
                    if hasattr(obj1, 'on_ground'):
                        obj1.on_ground = True
            else:
                obj1.y += overlap_y / 2
                obj2.y -= overlap_y / 2
                if obj2.vy > 0:
                    obj2.vy = 0
                    if hasattr(obj2, 'on_ground'):
                        obj2.on_ground = True