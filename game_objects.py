#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
游戏对象模型
定义马里奥游戏中所有对象的基类和具体实现
"""

class GameObject:
    """游戏对象基类"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0  # 水平速度
        self.vy = 0  # 垂直速度
        self.width = 1
        self.height = 1
    
    def update(self):
        """更新对象状态"""
        # 根据速度更新位置
        self.x += self.vx
        self.y += self.vy
    
    def collides_with(self, other):
        """检测与其他对象的碰撞"""
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)

class Player(GameObject):
    """玩家角色类"""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.lives = 3
        self.score = 0
        self.width = 1
        self.height = 2
        self.on_ground = False
        self.jumping = False
    
    def move_left(self):
        """向左移动"""
        self.vx = -1
    
    def move_right(self):
        """向右移动"""
        self.vx = 1
    
    def stop_moving(self):
        """停止水平移动"""
        self.vx = 0
    
    def jump(self):
        """跳跃"""
        if self.on_ground:
            self.vy = -12
            self.on_ground = False
            self.jumping = True
    
    def update(self):
        """更新玩家状态"""
        super().update()
        
        # 应用摩擦力
        if self.on_ground:
            self.vx *= 0.8
            if abs(self.vx) < 0.1:
                self.vx = 0
        
        # 限制最大速度
        if self.vx > 5:
            self.vx = 5
        elif self.vx < -5:
            self.vx = -5

class Enemy(GameObject):
    """敌人基类"""
    def __init__(self, x, y, enemy_type):
        super().__init__(x, y)
        self.type = enemy_type
        self.width = 1
        self.height = 1
        self.direction = -1  # -1表示向左，1表示向右
    
    def update(self):
        """更新敌人状态"""
        super().update()
        # 简单的巡逻行为
        self.vx = 0.5 * self.direction

class Item(GameObject):
    """道具类"""
    def __init__(self, x, y, item_type):
        super().__init__(x, y)
        self.type = item_type
        self.width = 1
        self.height = 1

class Block(GameObject):
    """方块类"""
    def __init__(self, x, y, block_type, content):
        super().__init__(x, y)
        self.type = block_type  # brick, question, used, pipe等
        self.content = content  # 方块内的内容（如金币、蘑菇等）
        self.width = 1
        self.height = 1