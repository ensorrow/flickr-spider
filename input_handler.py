#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
输入处理模块
处理用户的键盘输入并映射到游戏动作
"""

import curses

class InputHandler:
    """输入处理器"""
    def __init__(self):
        """初始化输入映射"""
        self.key_map = {
            curses.KEY_LEFT: "left",
            curses.KEY_RIGHT: "right",
            ord('a'): "left",
            ord('d'): "right",
            curses.KEY_UP: "jump",
            ord('w'): "jump",
            ord(' '): "jump",
            ord('q'): "quit",
            27: "quit"  # ESC键
        }
    
    def process_key(self, key):
        """处理按键输入"""
        if key in self.key_map:
            return self.key_map[key]
        return None
    
    def get_direction(self, key):
        """获取移动方向"""
        if key in [curses.KEY_LEFT, ord('a')]:
            return -1  # 左
        elif key in [curses.KEY_RIGHT, ord('d')]:
            return 1   # 右
        return 0       # 无移动