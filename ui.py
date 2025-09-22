import pygame
from config import CELL_SIZE, BLACK, WHITE, GREEN, RED

class UI:
    def __init__(self, screen):
        """初始化UI"""
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
    
    def draw_snake(self, snake_body):
        """绘制蛇"""
        for segment in snake_body:
            pygame.draw.rect(self.screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    
    def draw_food(self, food_position):
        """绘制食物"""
        pygame.draw.rect(self.screen, RED, pygame.Rect(food_position[0], food_position[1], CELL_SIZE, CELL_SIZE))
    
    def draw_score(self, score):
        """绘制得分"""
        score_text = self.font.render(f"Score: {score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
    
    def draw_game_over(self):
        """绘制游戏结束界面"""
        game_over_text = self.font.render("Game Over! Press R to restart", True, WHITE)
        text_rect = game_over_text.get_rect(center=(400, 300))
        self.screen.blit(game_over_text, text_rect)
    
    def draw_pause(self):
        """绘制暂停界面"""
        pause_text = self.font.render("PAUSED - Press SPACE to continue", True, WHITE)
        text_rect = pause_text.get_rect(center=(400, 300))
        self.screen.blit(pause_text, text_rect)