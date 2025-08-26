"""
底板類別模組
管理玩家控制的底板
"""

import pygame
from ..utils.colors import PADDLE_COLOR


class Paddle:
    """玩家操控的底板類別"""

    def __init__(
        self,
        brick_width,
        width_multiplier=2.5,
        height=14,
        y_offset=40,
        color=None,
        screen_width=800,
        screen_height=600,
        shrink_amount=5,
        min_width=40,
    ):
        """
        初始化底板\n
        brick_width: 磚塊寬度（用作寬度基準）\n
        width_multiplier: 寬度倍數\n
        height: 底板高度\n
        y_offset: 距離螢幕底部的距離\n
        color: 底板顏色，若為 None 則使用預設顏色\n
        screen_width: 螢幕寬度\n
        screen_height: 螢幕高度\n
        shrink_amount: 每次縮小的像素數\n
        min_width: 最小寬度\n
        """
        self.brick_width = brick_width
        self.width = int(brick_width * width_multiplier)
        self.height = height
        self.color = color if color else PADDLE_COLOR
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.shrink_amount = shrink_amount
        self.min_width = min_width

        # 初始位置置中，y 固定在底部上方
        start_x = (screen_width - self.width) // 2
        self.y = screen_height - y_offset
        self.rect = pygame.Rect(start_x, self.y, self.width, self.height)

    def update(self):
        """更新底板位置（跟隨滑鼠移動）"""
        mx, _ = pygame.mouse.get_pos()
        new_x = mx - self.width // 2
        # 限制在螢幕範圍內
        new_x = max(0, min(new_x, self.screen_width - self.width))
        self.rect.x = new_x

    def shrink(self):
        """縮小底板（擊中磚塊時調用）"""
        old_centerx = self.rect.centerx
        new_width = max(self.min_width, self.width - self.shrink_amount)

        if new_width != self.width:
            self.width = new_width
            self.rect.width = new_width
            self.rect.centerx = old_centerx
            # 確保不超出螢幕邊界
            self.rect.x = max(0, min(self.rect.x, self.screen_width - self.width))

    def draw(self, screen):
        """繪製底板"""
        pygame.draw.rect(screen, self.color, self.rect)

    def get_hit_factor(self, ball_x):
        """
        計算球撞擊底板的相對位置（用於改變反彈角度）\n
        ball_x: 球的 x 座標\n
        return: -1 到 1 之間的值，表示撞擊位置\n
        """
        return (ball_x - self.rect.centerx) / (self.width / 2)
