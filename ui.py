import pygame
from config import CELL_SIZE, BLACK, WHITE, GREEN, RED

class UI:
    def __init__(self, screen):
        """初始化UI"""
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def draw_snake(self, snake_body):
        """绘制蛇"""
        for i, segment in enumerate(snake_body):
            # 蛇头使用亮绿色，身体使用深绿色
            color = GREEN if i == 0 else (0, 200, 0)
            pygame.draw.rect(self.screen, color, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))
            # 添加边框使蛇身更清晰
            pygame.draw.rect(self.screen, BLACK, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE), 1)
    
    def draw_food(self, food_position):
        """绘制食物"""
        # 绘制红色食物
        pygame.draw.rect(self.screen, RED, pygame.Rect(food_position[0], food_position[1], CELL_SIZE, CELL_SIZE))
        # 添加边框
        pygame.draw.rect(self.screen, BLACK, pygame.Rect(food_position[0], food_position[1], CELL_SIZE, CELL_SIZE), 1)
    
    def draw_score(self, score):
        """绘制得分"""
        score_text = self.font.render(f"Score: {score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
    
    def draw_game_over(self):
        """绘制游戏结束界面"""
        # 半透明覆盖层
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("Game Over!", True, WHITE)
        text_rect = game_over_text.get_rect(center=(400, 250))
        self.screen.blit(game_over_text, text_rect)
        
        restart_text = self.small_font.render("Press R to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(400, 300))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_pause(self):
        """绘制暂停界面"""
        # 半透明覆盖层
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font.render("PAUSED", True, WHITE)
        text_rect = pause_text.get_rect(center=(400, 250))
        self.screen.blit(pause_text, text_rect)
        
        continue_text = self.small_font.render("Press SPACE to continue", True, WHITE)
        continue_rect = continue_text.get_rect(center=(400, 300))
        self.screen.blit(continue_text, continue_rect)