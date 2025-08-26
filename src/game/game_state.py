"""
遊戲狀態管理模組
管理遊戲的不同狀態（遊戲中、勝利、暫停等）
"""

from enum import Enum


class GameState(Enum):
    """遊戲狀態枚舉"""

    PLAYING = "playing"  # 遊戲進行中
    WAITING_TO_START = "waiting"  # 等待開始（球未發射）
    WIN = "win"  # 勝利
    GAME_OVER = "game_over"  # 遊戲結束
    PAUSED = "paused"  # 暫停


class GameStateManager:
    """遊戲狀態管理器"""

    def __init__(self):
        self.current_state = GameState.WAITING_TO_START
        self.score = 0
        self.level = 1

    def set_state(self, new_state):
        """設定新的遊戲狀態"""
        self.current_state = new_state

    def is_playing(self):
        """檢查是否在遊戲中"""
        return self.current_state == GameState.PLAYING

    def is_waiting(self):
        """檢查是否在等待開始"""
        return self.current_state == GameState.WAITING_TO_START

    def is_win(self):
        """檢查是否勝利"""
        return self.current_state == GameState.WIN

    def is_game_over(self):
        """檢查是否遊戲結束"""
        return self.current_state == GameState.GAME_OVER

    def add_score(self, points):
        """增加分數"""
        self.score += points

    def reset_score(self):
        """重置分數"""
        self.score = 0

    def next_level(self):
        """進入下一關"""
        self.level += 1
        self.current_state = GameState.WAITING_TO_START

    def reset_level(self):
        """重置關卡"""
        self.level = 1
