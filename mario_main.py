#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
马里奥游戏主程序
基于终端的马里奥游戏实现
"""

import curses
import time
from game_objects import Player, Enemy, Item, Block
from input_handler import InputHandler
from physics import PhysicsEngine
from level import Level
from renderer import Renderer
from game_state import GameState

class MarioGame:
    def __init__(self, stdscr):
        """初始化游戏"""
        self.stdscr = stdscr
        self.game_state = GameState()
        self.input_handler = InputHandler()
        self.physics_engine = PhysicsEngine()
        self.renderer = Renderer(stdscr)
        self.level = None
        self.player = None
        self.enemies = []
        self.items = []
        self.blocks = []
        
        # 初始化curses
        curses.curs_set(0)  # 隐藏光标
        self.stdscr.nodelay(True)  # 非阻塞输入
        self.stdscr.timeout(100)  # 设置输入超时
        
        # 初始化游戏
        self.init_game()
    
    def init_game(self):
        """初始化游戏内容"""
        # 创建第一关
        self.level = Level(1)
        
        # 创建玩家
        self.player = Player(5, 20)
        
        # 创建敌人
        self.enemies = [
            Enemy(20, 20, "goomba"),
            Enemy(30, 20, "koopa")
        ]
        
        # 创建道具
        self.items = [
            Item(15, 18, "coin"),
            Item(25, 15, "mushroom")
        ]
        
        # 创建方块
        self.blocks = [
            Block(10, 18, "brick", None),
            Block(15, 15, "question", "coin"),
            Block(20, 12, "brick", None)
        ]
    
    def handle_input(self):
        """处理用户输入"""
        key = self.stdscr.getch()
        if key != -1:  # 有输入
            action = self.input_handler.process_key(key)
            if action == "quit":
                self.game_state.running = False
            elif action == "left":
                self.player.move_left()
            elif action == "right":
                self.player.move_right()
            elif action == "jump":
                self.player.jump()
    
    def update_game_state(self):
        """更新游戏状态"""
        # 更新玩家状态
        self.physics_engine.apply_gravity(self.player)
        self.player.update()
        
        # 更新敌人状态
        for enemy in self.enemies:
            self.physics_engine.apply_gravity(enemy)
            enemy.update()
        
        # 碰撞检测
        self.check_collisions()
        
        # 检查游戏结束条件
        if self.player.lives <= 0:
            self.game_state.game_over = True
    
    def check_collisions(self):
        """检查碰撞"""
        # 玩家与敌人的碰撞
        for enemy in self.enemies[:]:  # 使用副本避免在迭代时修改列表
            if self.player.collides_with(enemy):
                if self.player.vy > 0 and self.player.y < enemy.y:  # 从上方踩踏
                    self.enemies.remove(enemy)
                    self.player.score += 100
                    self.player.vy = -8  # 跳跃效果
                else:  # 被敌人撞击
                    self.player.lives -= 1
                    self.player.x, self.player.y = 5, 20  # 重生位置
        
        # 玩家与道具的碰撞
        for item in self.items[:]:
            if self.player.collides_with(item):
                if item.type == "coin":
                    self.player.score += 200
                elif item.type == "mushroom":
                    self.player.lives += 1
                self.items.remove(item)
        
        # 玩家与方块的碰撞
        for block in self.blocks:
            if self.player.collides_with(block):
                if block.type == "question" and block.content:
                    # 生成新道具
                    new_item = Item(block.x, block.y - 1, block.content)
                    self.items.append(new_item)
                    block.content = None  # 清空方块内容
                    block.type = "used"  # 改变方块外观
    
    def render(self):
        """渲染游戏画面"""
        self.renderer.clear()
        self.renderer.draw_level(self.level)
        self.renderer.draw_player(self.player)
        for enemy in self.enemies:
            self.renderer.draw_enemy(enemy)
        for item in self.items:
            self.renderer.draw_item(item)
        for block in self.blocks:
            self.renderer.draw_block(block)
        self.renderer.draw_ui(self.player.score, self.player.lives, self.game_state.current_level)
        self.renderer.refresh()
    
    def run(self):
        """游戏主循环"""
        self.game_state.running = True
        
        while self.game_state.running:
            # 处理输入
            self.handle_input()
            
            # 更新游戏状态
            if not self.game_state.paused and not self.game_state.game_over:
                self.update_game_state()
            
            # 渲染画面
            self.render()
            
            # 控制帧率
            time.sleep(0.05)
        
        # 游戏结束
        if self.game_state.game_over:
            self.renderer.show_game_over()
        else:
            self.renderer.show_exit_message()

def main(stdscr):
    """主函数"""
    game = MarioGame(stdscr)
    game.run()

if __name__ == "__main__":
    curses.wrapper(main)