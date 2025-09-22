import random
import pygame
from config import CELL_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT

class Food:
    def __init__(self):
        """初始化食物"""
        self.position = (0, 0)
        self.generate_new_food([])
    
    def generate_new_food(self, snake_body):
        """生成新的食物位置，确保不与蛇身重叠"""
        while True:
            # 在游戏区域内随机生成坐标
            x = random.randrange(0, WINDOW_WIDTH, CELL_SIZE)
            y = random.randrange(0, WINDOW_HEIGHT, CELL_SIZE)
            self.position = (x, y)
            
            # 确保生成位置不与蛇身重叠
            if self.position not in snake_body:
                break
    
    def get_position(self):
        """获取食物位置"""
        return self.position