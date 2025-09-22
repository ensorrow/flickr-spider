import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from snake import Snake
from food import Food
from config import WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE

class TestSnake(unittest.TestCase):
    
    def setUp(self):
        """测试前的准备工作"""
        self.snake = Snake()
    
    def test_initialization(self):
        """测试蛇的初始化"""
        self.assertEqual(self.snake.length, 3)
        self.assertEqual(len(self.snake.get_body()), 3)
        self.assertEqual(self.snake.direction, (CELL_SIZE, 0))
    
    def test_move(self):
        """测试蛇的移动"""
        initial_head = self.snake.get_head_position()
        self.snake.move()
        new_head = self.snake.get_head_position()
        
        # 检查蛇头是否向右移动了一个单元
        self.assertEqual(new_head[0], initial_head[0] + CELL_SIZE)
        self.assertEqual(new_head[1], initial_head[1])
    
    def test_change_direction(self):
        """测试改变方向"""
        # 测试向上移动
        self.snake.change_direction((0, -CELL_SIZE))
        self.assertEqual(self.snake.direction, (0, -CELL_SIZE))
        
        # 测试不能直接反向移动
        self.snake.change_direction((0, CELL_SIZE))  # 尝试向下移动（反向）
        self.assertEqual(self.snake.direction, (0, -CELL_SIZE))  # 应该保持原方向
    
    def test_grow(self):
        """测试蛇增长"""
        initial_length = len(self.snake.get_body())
        self.snake.grow()
        self.snake.move()
        new_length = len(self.snake.get_body())
        
        # 蛇应该增长一个单位
        self.assertEqual(new_length, initial_length + 1)
    
    def test_collision_with_wall(self):
        """测试与墙壁的碰撞"""
        # 创建一个靠近右边界的蛇
        self.snake.body = [(WINDOW_WIDTH - CELL_SIZE, WINDOW_HEIGHT // 2)]
        self.snake.direction = (CELL_SIZE, 0)  # 向右移动
        
        self.snake.move()  # 移动出边界
        self.assertTrue(self.snake.check_collision())
    
    def test_collision_with_self(self):
        """测试与自身的碰撞"""
        # 创建一个会撞到自己的蛇
        self.snake.body = [
            (100, 100),  # 头部
            (80, 100),
            (80, 120),
            (100, 120),
            (100, 100)   # 尾部与头部重叠，模拟碰撞
        ]
        self.assertTrue(self.snake.check_collision())

class TestFood(unittest.TestCase):
    
    def setUp(self):
        """测试前的准备工作"""
        self.food = Food()
    
    def test_initialization(self):
        """测试食物的初始化"""
        self.assertIsNotNone(self.food.get_position())
    
    def test_generate_new_food(self):
        """测试生成新食物"""
        snake_body = [(0, 0), (20, 0), (40, 0)]
        old_position = self.food.get_position()
        self.food.generate_new_food(snake_body)
        new_position = self.food.get_position()
        
        # 新位置不应该与蛇身重叠
        self.assertNotIn(new_position, snake_body)

if __name__ == '__main__':
    unittest.main()