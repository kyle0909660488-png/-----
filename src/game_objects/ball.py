"""
球類別模組
管理遊戲中的球物件
"""

import pygame
from ..utils.colors import BALL_COLOR


class Ball:
    """遊戲中的球類別，負責移動和碰撞檢測"""

    def __init__(
        self,
        x=400,
        y=500,
        radius=8,
        color=None,
        x_speed=5,
        y_speed=-5,
        screen_width=800,
        screen_height=600,
        follow_distance=5,
    ):
        """
        初始化球

        Args:
            x, y (float): 初始位置
            radius (int): 球的半徑
            color (tuple): 球的顏色，若為 None 則使用預設顏色
            x_speed, y_speed (float): 水平和垂直速度
            screen_width, screen_height (int): 螢幕尺寸
            follow_distance (int): 跟隨底板時的距離
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color if color else BALL_COLOR
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.follow_distance = follow_distance
        self.started = False  # 是否已開始移動

        # 建立碰撞檢測用的矩形區域
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)

    def move(self):
        """移動球的位置"""
        if self.started:
            self.x += self.x_speed
            self.y += self.y_speed
            self._update_rect()

    def _update_rect(self):
        """更新碰撞檢測矩形"""
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    def check_wall_collision(self):
        """檢查球與視窗邊界的碰撞"""
        # 左右邊界碰撞
        if self.x - self.radius <= 0 or self.x + self.radius >= self.screen_width:
            self.x_speed = -self.x_speed
            # 防止球卡在邊界外
            if self.x - self.radius <= 0:
                self.x = self.radius
            else:
                self.x = self.screen_width - self.radius
            self._update_rect()

        # 上邊界碰撞
        if self.y - self.radius <= 0:
            self.y_speed = -self.y_speed
            self.y = self.radius
            self._update_rect()

    def check_paddle_collision(self, paddle):
        """
        檢查球與底板的碰撞

        Args:
            paddle: 底板物件

        Returns:
            bool: 是否發生碰撞
        """
        if self.rect.colliderect(paddle.rect) and self.y_speed > 0:
            # 計算球撞擊底板的相對位置
            hit_factor = paddle.get_hit_factor(self.x)

            # 根據撞擊位置改變球的水平速度
            self.x_speed = hit_factor * abs(self.y_speed)
            self.y_speed = -abs(self.y_speed)

            # 確保球不會卡在底板裡
            self.y = paddle.rect.top - self.radius
            self._update_rect()
            return True
        return False

    def bounce_horizontal(self):
        """水平反彈"""
        self.x_speed = -self.x_speed

    def bounce_vertical(self):
        """垂直反彈"""
        self.y_speed = -self.y_speed

    def is_out_of_bounds(self):
        """檢查球是否掉出螢幕下方"""
        return self.y - self.radius > self.screen_height

    def follow_paddle(self, paddle):
        """讓球跟隨底板移動（僅在球尚未發射時）"""
        if not self.started:
            self.x = paddle.rect.centerx
            self.y = paddle.rect.top - self.radius - self.follow_distance
            self._update_rect()

    def start(self):
        """開始發球"""
        self.started = True

    def reset(self, x=None, y=None, paddle=None):
        """
        重置球的位置和狀態

        Args:
            x, y (float): 新位置，若為 None 則使用預設值或跟隨底板
            paddle: 底板物件，用於自動定位
        """
        if paddle and x is None and y is None:
            # 自動跟隨底板位置
            self.x = paddle.rect.centerx
            self.y = paddle.rect.top - self.radius - self.follow_distance
        else:
            self.x = x if x is not None else self.screen_width // 2
            self.y = y if y is not None else self.screen_height - 60

        self.started = False
        self._update_rect()

    def draw(self, screen):
        """繪製球"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
