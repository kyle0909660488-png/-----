"""
遊戲引擎主類別
整合所有遊戲元素並管理遊戲主迴圈
"""

import pygame
import sys

from ..game_objects import Ball, Brick, Paddle
from ..utils.font_loader import load_chinese_font
from ..utils.colors import BACKGROUND_COLOR, TEXT_COLOR, INFO_TEXT_COLOR
from .game_state import GameState, GameStateManager


class GameEngine:
    """遊戲引擎主類別"""

    def __init__(self, config):
        """
        初始化遊戲引擎\n
        config: 設定模組物件\n
        """
        self.config = config
        self.clock = pygame.time.Clock()

        # 初始化 pygame
        pygame.init()

        # 設定視窗
        self.screen = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        )
        pygame.display.set_caption(config.WINDOW_TITLE)

        # 遊戲狀態管理器
        self.game_state = GameStateManager()

        # 字型設定
        self.score_font = load_chinese_font(config.SCORE_FONT_SIZE)
        self.info_font = load_chinese_font(config.INFO_FONT_SIZE)
        self.win_font = load_chinese_font(config.WIN_FONT_SIZE)

        # 初始化遊戲物件
        self.init_game_objects()

    def init_game_objects(self):
        """初始化遊戲物件"""
        # 建立磚牆
        self.brick_wall = Brick(
            cols=self.config.BRICK_COLS,
            rows=self.config.BRICK_ROWS,
            brick_width=self.config.BRICK_WIDTH,
            brick_height=self.config.BRICK_HEIGHT,
            padding=self.config.BRICK_PADDING,
            top_margin=self.config.BRICK_TOP_MARGIN,
            screen_width=self.config.WINDOW_WIDTH,
            special_count=self.config.SPECIAL_BRICK_COUNT,
        )

        # 建立底板
        self.paddle = Paddle(
            brick_width=self.config.BRICK_WIDTH,
            width_multiplier=self.config.PADDLE_WIDTH_MULTIPLIER,
            height=self.config.PADDLE_HEIGHT,
            y_offset=self.config.PADDLE_Y_OFFSET,
            color=self.config.PADDLE_COLOR,
            screen_width=self.config.WINDOW_WIDTH,
            screen_height=self.config.WINDOW_HEIGHT,
            shrink_amount=self.config.PADDLE_SHRINK_AMOUNT,
            min_width=self.config.PADDLE_MIN_WIDTH,
        )

        # 建立球
        self.ball = Ball(
            x=self.config.WINDOW_WIDTH // 2,
            y=self.config.WINDOW_HEIGHT - 60,
            radius=self.config.BALL_RADIUS,
            color=self.config.BALL_COLOR,
            x_speed=self.config.BALL_SPEED_X,
            y_speed=self.config.BALL_SPEED_Y,
            screen_width=self.config.WINDOW_WIDTH,
            screen_height=self.config.WINDOW_HEIGHT,
            follow_distance=self.config.BALL_FOLLOW_DISTANCE,
        )

        # 重置遊戲狀態
        self.game_state.reset_score()
        self.game_state.set_state(GameState.WAITING_TO_START)

    def handle_events(self):
        """處理遊戲事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # 滑鼠點擊或空白鍵發球
            if event.type == pygame.MOUSEBUTTONDOWN or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
            ):
                if self.game_state.is_waiting():
                    self.ball.start()
                    self.game_state.set_state(GameState.PLAYING)

            # 按 E 鍵在勝利後開始下一輪
            if event.type == pygame.KEYDOWN:
                is_e_key_pressed = event.key == pygame.K_e or (
                    hasattr(event, "unicode")
                    and event.unicode
                    and event.unicode.lower() == "e"
                )
                if is_e_key_pressed and self.game_state.is_win():
                    self.init_game_objects()

        return True

    def update(self):
        """更新遊戲邏輯"""
        # 更新底板
        self.paddle.update()

        # 根據遊戲狀態更新球
        if self.game_state.is_waiting():
            self.ball.follow_paddle(self.paddle)
        elif self.game_state.is_playing():
            self.ball.move()
            self._check_collisions()
            self._check_win_condition()
            self._check_ball_out_of_bounds()

    def _check_collisions(self):
        """檢查各種碰撞"""
        # 牆壁碰撞
        self.ball.check_wall_collision()

        # 底板碰撞
        self.ball.check_paddle_collision(self.paddle)

        # 磚塊碰撞
        is_collision_hit, hit_count, collision_direction = (
            self.brick_wall.check_collision(self.ball.rect)
        )
        if is_collision_hit:
            # 增加分數
            self.game_state.add_score(self.config.SCORE_PER_BRICK * hit_count)

            # 縮小底板
            for _ in range(hit_count):
                self.paddle.shrink()

            # 反彈球
            if collision_direction == "horizontal":
                self.ball.bounce_horizontal()
            else:
                self.ball.bounce_vertical()

    def _check_win_condition(self):
        """檢查勝利條件"""
        if self.brick_wall.get_remaining_bricks_count() == 0:
            self.game_state.set_state(GameState.WIN)
            self.ball.started = False  # 停止球的移動

    def _check_ball_out_of_bounds(self):
        """檢查球是否掉出邊界"""
        if self.ball.is_out_of_bounds():
            self.ball.reset(paddle=self.paddle)
            self.game_state.set_state(GameState.WAITING_TO_START)

    def draw(self):
        """繪製所有遊戲元素"""
        # 清除螢幕
        self.screen.fill(BACKGROUND_COLOR)

        # 繪製遊戲物件
        self.brick_wall.draw(self.screen)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)

        # 繪製 UI
        self._draw_ui()

        # 更新顯示
        pygame.display.update()

    def _draw_ui(self):
        """繪製使用者介面"""
        # 繪製分數
        score_text = f"分數: {self.game_state.score}"
        score_surf = self.score_font.render(score_text, True, TEXT_COLOR)
        score_rect = score_surf.get_rect(
            topright=(
                self.config.WINDOW_WIDTH - self.config.TEXT_PADDING,
                self.config.TEXT_PADDING,
            )
        )
        self.screen.blit(score_surf, score_rect)

        # 繪製提示訊息
        if self.game_state.is_waiting():
            info_text = "滑鼠點擊或按空白鍵發球"
            info_surf = self.info_font.render(info_text, True, INFO_TEXT_COLOR)
            info_rect = info_surf.get_rect(
                topright=(
                    self.config.WINDOW_WIDTH - self.config.TEXT_PADDING,
                    score_rect.bottom + 6,
                )
            )
            self.screen.blit(info_surf, info_rect)

        # 繪製勝利訊息
        if self.game_state.is_win():
            win_surf = self.win_font.render("你贏了！", True, TEXT_COLOR)
            win_rect = win_surf.get_rect(
                center=(
                    self.config.WINDOW_WIDTH // 2,
                    self.config.WINDOW_HEIGHT // 2 - 20,
                )
            )
            self.screen.blit(win_surf, win_rect)

            next_surf = self.info_font.render("按 E 開始下一輪", True, INFO_TEXT_COLOR)
            next_rect = next_surf.get_rect(
                center=(
                    self.config.WINDOW_WIDTH // 2,
                    self.config.WINDOW_HEIGHT // 2 + 30,
                )
            )
            self.screen.blit(next_surf, next_rect)

    def run(self):
        """運行遊戲主迴圈"""
        running = True

        while running:
            # 控制 FPS
            self.clock.tick(self.config.FPS)

            # 處理事件
            running = self.handle_events()

            # 更新遊戲邏輯
            self.update()

            # 繪製畫面
            self.draw()

        # 退出遊戲
        pygame.quit()
        sys.exit()
