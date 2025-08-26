"""
磚塊類別模組
管理遊戲中的磚塊牆
"""

import pygame
import random
from ..utils.colors import (
    BRICK_COLORS,
    SPECIAL_BRICK_FLASH_COLORS,
    get_text_color_for_background,
)
from ..utils.font_loader import load_chinese_font


class Brick:
    """磚塊牆類別，負責管理整面磚塊牆的生成、繪製和碰撞檢測"""

    def __init__(
        self,
        cols=10,
        rows=5,
        brick_width=60,
        brick_height=20,
        padding=5,
        top_margin=50,
        screen_width=800,
        special_count=7,
    ):
        """
        產生一整面磚牆（cols x rows）並自動置中

        Args:
            cols (int): 磚塊欄數
            rows (int): 磚塊列數
            brick_width (int): 磚塊寬度
            brick_height (int): 磚塊高度
            padding (int): 磚塊間距
            top_margin (int): 磚牆上方邊距
            screen_width (int): 螢幕寬度（用於置中計算）
            special_count (int): 特殊爆炸磚塊數量
        """
        self.cols = cols
        self.rows = rows
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.padding = padding
        self.top_margin = top_margin

        # 計算整個磚牆的寬度以便置中
        total_width = cols * brick_width + (cols - 1) * padding
        start_x = int((screen_width - total_width) / 2)

        # 建立每個磚塊的資料結構
        self.bricks = []
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (brick_width + padding)
                y = top_margin + row * (brick_height + padding)
                # 每個磚塊使用不同的顏色（以 column 為主）
                color = BRICK_COLORS[col % len(BRICK_COLORS)]
                self.bricks.append(
                    {
                        "rect": pygame.Rect(x, y, brick_width, brick_height),
                        "color": color,
                        "is_hit": False,
                        "row": row,
                        "col": col,
                        "is_special": False,  # 特殊炸裂磚塊標記
                    }
                )

        # 隨機選擇特殊磚塊
        self._set_special_bricks(special_count)

    def _set_special_bricks(self, special_count):
        """隨機設定特殊磚塊"""
        actual_count = min(special_count, len(self.bricks))
        special_indices = random.sample(range(len(self.bricks)), k=actual_count)
        for idx in special_indices:
            self.bricks[idx]["is_special"] = True

    def draw(self, screen):
        """繪製整面磚牆（未被擊中的磚塊才繪製）"""
        for brick in self.bricks:
            if not brick["is_hit"]:
                # 繪製磚塊本體
                pygame.draw.rect(screen, brick["color"], brick["rect"])

                # 若為特殊磚塊，加上閃爍效果和標示
                if brick.get("is_special", False):
                    self._draw_special_brick_effects(screen, brick)

    def _draw_special_brick_effects(self, screen, brick):
        """繪製特殊磚塊的視覺效果"""
        # 閃爍外框效果
        tick = pygame.time.get_ticks()
        phase = (tick // 300) % 2
        outline_color = SPECIAL_BRICK_FLASH_COLORS[phase]
        pygame.draw.rect(screen, outline_color, brick["rect"], 3)

        # 在磚塊中央顯示中文字『爆』
        try:
            font_size = max(12, int(min(brick["rect"].height * 0.9, 24)))
            font = load_chinese_font(font_size)
            text_color = get_text_color_for_background(brick["color"])
            text_surf = font.render("爆", True, text_color)
            text_rect = text_surf.get_rect(center=brick["rect"].center)
            screen.blit(text_surf, text_rect)
        except Exception:
            # 若字型載入失敗，保留外框作為標示
            pass

    def get_remaining_bricks_count(self):
        """取得剩餘磚塊數量"""
        return sum(1 for brick in self.bricks if not brick["is_hit"])

    def check_collision(self, ball_rect):
        """
        檢查球與磚塊的碰撞

        Args:
            ball_rect (pygame.Rect): 球的碰撞矩形

        Returns:
            tuple: (is_hit, hit_count, collision_direction)
                   is_hit: 是否有碰撞
                   hit_count: 被擊中的磚塊數量（包含爆炸連帶）
                   collision_direction: 碰撞方向 ('horizontal' 或 'vertical')
        """
        for brick in self.bricks:
            if not brick["is_hit"] and ball_rect.colliderect(brick["rect"]):
                # 標記磚塊被擊中
                brick["is_hit"] = True
                hit_count = 1

                # 若為特殊磚塊，觸發爆炸效果
                if brick.get("is_special", False):
                    hit_count += self._explode_around(brick["row"], brick["col"])

                # 計算碰撞方向
                collision_direction = self._calculate_collision_direction(
                    ball_rect, brick["rect"]
                )

                return True, hit_count, collision_direction

        return False, 0, None

    def _explode_around(self, center_row, center_col):
        """爆炸效果：破壞周圍 3x3 範圍的磚塊"""
        additional_hits = 0
        for brick in self.bricks:
            if not brick["is_hit"]:
                if (
                    abs(brick["row"] - center_row) <= 1
                    and abs(brick["col"] - center_col) <= 1
                ):
                    brick["is_hit"] = True
                    additional_hits += 1
        return additional_hits

    def _calculate_collision_direction(self, ball_rect, brick_rect):
        """計算碰撞方向"""
        ball_center_x = ball_rect.centerx
        ball_center_y = ball_rect.centery
        brick_center_x = brick_rect.centerx
        brick_center_y = brick_rect.centery

        dx = abs(ball_center_x - brick_center_x)
        dy = abs(ball_center_y - brick_center_y)

        # 根據撞擊位置比例判斷主要碰撞方向
        if dx / (brick_rect.width / 2) > dy / (brick_rect.height / 2):
            return "horizontal"
        else:
            return "vertical"
