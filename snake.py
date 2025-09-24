import pygame
from config import CELL_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT

class Snake:
    def __init__(self):
        """初始化蛇"""
        self.length = 3
        # 初始位置在屏幕中心偏左
        self.body = [(WINDOW_WIDTH // 2 - i * CELL_SIZE, WINDOW_HEIGHT // 2) for i in range(self.length)]
        # 初始方向向右
        self.direction = (CELL_SIZE, 0)
        self.grow_pending = False  # 是否需要增长
    
    def move(self):
        """移动蛇"""
        # 计算新的蛇头位置
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        # 将新头部插入到身体列表开头
        self.body.insert(0, new_head)
        
        # 如果不需要增长，则移除尾部
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False
            self.length += 1
    
    def change_direction(self, new_direction):
        """改变蛇的移动方向"""
        # 防止蛇反向移动（不能直接掉头）
        dir_x, dir_y = self.direction
        new_dir_x, new_dir_y = new_direction
        
        # 只有当新方向与当前方向不相反时才改变方向
        if (dir_x, dir_y) != (-new_dir_x, -new_dir_y):
            self.direction = new_direction
    
    def grow(self):
        """使蛇增长"""
        self.grow_pending = True
    
    def check_collision(self):
        """检查碰撞"""
        head_x, head_y = self.body[0]
        
        # 检查是否撞墙
        if (head_x < 0 or head_x >= WINDOW_WIDTH or 
            head_y < 0 or head_y >= WINDOW_HEIGHT):
            return True
        
        # 检查是否撞到自己
        if self.body[0] in self.body[1:]:
            return True
        
        return False
    
    def get_head_position(self):
        """获取蛇头位置"""
        return self.body[0]
    
    def get_body(self):
        """获取蛇身位置列表"""
        return self.body