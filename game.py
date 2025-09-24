import pygame
import sys
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, CELL_SIZE
from snake import Snake
from food import Food
from ui import UI

class Game:
    def __init__(self):
        """初始化游戏"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("贪吃蛇游戏")
        self.clock = pygame.time.Clock()
        
        # 游戏对象
        self.snake = Snake()
        self.food = Food()
        self.ui = UI(self.screen)
        
        # 游戏状态
        self.score = 0
        self.game_over = False
        self.paused = False
        
        # 生成初始食物，确保不与蛇身重叠
        self.food.generate_new_food(self.snake.get_body())
    
    def handle_events(self):
        """处理用户输入"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction((0, -CELL_SIZE))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, CELL_SIZE))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-CELL_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((CELL_SIZE, 0))
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
        return True
    
    def update(self):
        """更新游戏状态"""
        if self.game_over or self.paused:
            return
        
        # 移动蛇
        self.snake.move()
        
        # 检查碰撞
        if self.snake.check_collision():
            self.game_over = True
            return
        
        # 检查是否吃到食物
        if self.snake.get_head_position() == self.food.get_position():
            self.snake.grow()
            self.score += 10
            self.food.generate_new_food(self.snake.get_body())
    
    def render(self):
        """渲染游戏画面"""
        self.screen.fill((0, 0, 0))  # 填充黑色背景
        
        if not self.game_over:
            # 绘制蛇和食物
            self.ui.draw_snake(self.snake.get_body())
            self.ui.draw_food(self.food.get_position())
        
        # 绘制得分
        self.ui.draw_score(self.score)
        
        # 绘制游戏结束或暂停界面
        if self.game_over:
            self.ui.draw_game_over()
        elif self.paused:
            self.ui.draw_pause()
        
        pygame.display.flip()
    
    def restart_game(self):
        """重新开始游戏"""
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.paused = False
        # 重新生成食物，确保不与蛇身重叠
        self.food.generate_new_food(self.snake.get_body())
    
    def run(self):
        """运行游戏主循环"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()