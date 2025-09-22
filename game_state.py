#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
游戏状态管理模块
管理游戏的整体状态，如运行、暂停、游戏结束等
"""

class GameState:
    """游戏状态管理器"""
    def __init__(self):
        """初始化游戏状态"""
        self.running = False
        self.paused = False
        self.game_over = False
        self.current_level = 1
        self.score = 0
        self.lives = 3
        self.high_score = 0
    
    def start_game(self):
        """开始游戏"""
        self.running = True
        self.paused = False
        self.game_over = False
        self.current_level = 1
        self.score = 0
        self.lives = 3
    
    def pause_game(self):
        """暂停游戏"""
        if self.running and not self.game_over:
            self.paused = not self.paused
    
    def resume_game(self):
        """恢复游戏"""
        self.paused = False
    
    def end_game(self):
        """结束游戏"""
        self.running = False
        self.game_over = True
        # 更新最高分
        if self.score > self.high_score:
            self.high_score = self.score
    
    def next_level(self):
        """进入下一关"""
        self.current_level += 1
        self.score += 1000  # 过关奖励
    
    def reset_level(self):
        """重置当前关卡"""
        self.score = max(0, self.score - 500)  # 死亡惩罚
        self.lives = max(0, self.lives - 1)
    
    def is_running(self):
        """检查游戏是否正在运行"""
        return self.running and not self.game_over
    
    def is_paused(self):
        """检查游戏是否已暂停"""
        return self.paused
    
    def is_game_over(self):
        """检查游戏是否结束"""
        return self.game_over
    
    def get_score(self):
        """获取当前分数"""
        return self.score
    
    def get_lives(self):
        """获取剩余生命"""
        return self.lives
    
    def get_current_level(self):
        """获取当前关卡"""
        return self.current_level
    
    def get_high_score(self):
        """获取最高分"""
        return self.high_score
    
    def add_score(self, points):
        """增加分数"""
        self.score += points