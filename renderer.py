#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
渲染系统模块
负责在终端中渲染游戏画面
"""

import curses

class Renderer:
    """渲染器"""
    def __init__(self, stdscr):
        """初始化渲染器"""
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.camera_x = 0
        self.camera_y = 0
    
    def clear(self):
        """清空屏幕"""
        self.stdscr.clear()
    
    def refresh(self):
        """刷新屏幕"""
        self.stdscr.refresh()
    
    def draw_level(self, level):
        """绘制关卡"""
        # 绘制关卡地形
        for y in range(min(level.get_height(), self.height - 1)):
            for x in range(min(level.get_width(), self.width - 1)):
                tile = level.get_tile(x, y)
                if tile != ' ':
                    try:
                        self.stdscr.addch(y, x, tile)
                    except curses.error:
                        pass  # 忽略边界错误
    
    def draw_player(self, player):
        """绘制玩家"""
        try:
            # 简单的玩家表示
            screen_x = int(player.x - self.camera_x)
            screen_y = int(player.y - self.camera_y)
            
            if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
                self.stdscr.addch(screen_y, screen_x, 'M')
        except curses.error:
            pass  # 忽略边界错误
    
    def draw_enemy(self, enemy):
        """绘制敌人"""
        try:
            screen_x = int(enemy.x - self.camera_x)
            screen_y = int(enemy.y - self.camera_y)
            
            if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
                if enemy.type == "goomba":
                    self.stdscr.addch(screen_y, screen_x, 'g')
                elif enemy.type == "koopa":
                    self.stdscr.addch(screen_y, screen_x, 'k')
        except curses.error:
            pass  # 忽略边界错误
    
    def draw_item(self, item):
        """绘制道具"""
        try:
            screen_x = int(item.x - self.camera_x)
            screen_y = int(item.y - self.camera_y)
            
            if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
                if item.type == "coin":
                    self.stdscr.addch(screen_y, screen_x, 'o')
                elif item.type == "mushroom":
                    self.stdscr.addch(screen_y, screen_x, 'm')
        except curses.error:
            pass  # 忽略边界错误
    
    def draw_block(self, block):
        """绘制方块"""
        try:
            screen_x = int(block.x - self.camera_x)
            screen_y = int(block.y - self.camera_y)
            
            if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
                if block.type == "brick":
                    self.stdscr.addch(screen_y, screen_x, '#')
                elif block.type == "question":
                    self.stdscr.addch(screen_y, screen_x, '?')
                elif block.type == "used":
                    self.stdscr.addch(screen_y, screen_x, '-')
        except curses.error:
            pass  # 忽略边界错误
    
    def draw_ui(self, score, lives, level):
        """绘制UI界面"""
        try:
            # 绘制分数
            score_text = f"Score: {score}"
            self.stdscr.addstr(0, 0, score_text)
            
            # 绘制生命值
            lives_text = f"Lives: {lives}"
            self.stdscr.addstr(0, 15, lives_text)
            
            # 绘制关卡信息
            level_text = f"Level: {level}"
            self.stdscr.addstr(0, 30, level_text)
            
            # 绘制控制说明
            controls_text = "Controls: A/D/W/SPACE - Move, Q/ESC - Quit"
            self.stdscr.addstr(self.height - 1, 0, controls_text[:self.width-1])
        except curses.error:
            pass  # 忽略边界错误
    
    def show_game_over(self):
        """显示游戏结束画面"""
        try:
            self.stdscr.clear()
            game_over_text = "GAME OVER"
            score_text = "Final Score: {}"
            
            # 居中显示
            center_y = self.height // 2
            center_x = (self.width - len(game_over_text)) // 2
            
            self.stdscr.addstr(center_y, center_x, game_over_text)
            self.stdscr.addstr(center_y + 2, center_x, score_text)
            self.stdscr.addstr(center_y + 4, center_x, "Press any key to exit...")
            self.stdscr.refresh()
            
            # 等待用户按键
            self.stdscr.getch()
        except curses.error:
            pass  # 忽略边界错误
    
    def show_exit_message(self):
        """显示退出消息"""
        try:
            self.stdscr.clear()
            exit_text = "Thanks for playing!"
            self.stdscr.addstr(self.height // 2, (self.width - len(exit_text)) // 2, exit_text)
            self.stdscr.refresh()
            curses.napms(1000)  # 等待1秒
        except curses.error:
            pass  # 忽略边界错误
    
    def update_camera(self, player_x, player_y):
        """更新摄像机位置（视角跟随玩家）"""
        self.camera_x = player_x - self.width // 2
        self.camera_y = player_y - self.height // 2
        
        # 边界检查
        if self.camera_x < 0:
            self.camera_x = 0
        if self.camera_y < 0:
            self.camera_y = 0