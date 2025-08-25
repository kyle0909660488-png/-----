######################載入套件######################
import pygame
import sys


######################物件類別######################
class Brick:
    def __init__(
        self,
        cols=10,
        rows=5,
        brick_width=60,
        brick_height=20,
        padding=5,
        top_margin=50,
        screen_width=800,
    ):
        """產生一整面磚牆（cols x rows）並自動置中。

        參數:
        cols, rows: 欄數與列數（預設 10 x 5）
        brick_width, brick_height: 每個磚塊的寬高
        padding: 磚塊之間的間距
        top_margin: 磚牆上方與視窗上緣的距離
        screen_width: 用來計算置中的視窗寬度
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

        # 準備顏色（每一列或每一欄顏色不同）
        palette = [
            (255, 99, 71),
            (255, 165, 0),
            (255, 215, 0),
            (144, 238, 144),
            (135, 206, 250),
            (216, 191, 216),
            (173, 216, 230),
            (240, 128, 128),
            (255, 182, 193),
            (152, 251, 152),
        ]

        # 建立每個磚塊的資料結構
        self.bricks = []
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (brick_width + padding)
                y = top_margin + row * (brick_height + padding)
                # 每個磚塊使用 palette 中不同的顏色（以 column 為主），若不足則循環
                color = palette[col % len(palette)]
                self.bricks.append(
                    {
                        "rect": pygame.Rect(x, y, brick_width, brick_height),
                        "color": color,
                        "is_hit": False,
                    }
                )

    def draw(self, screen):
        """繪製整面磚牆（未被擊中的磚塊才繪製）。"""
        for b in self.bricks:
            if not b["is_hit"]:
                pygame.draw.rect(screen, b["color"], b["rect"])


class Paddle:
    """玩家操控的底板（以 Brick 物件的 brick_width 作為參考寬度）。

    行為:
    - 寬度會比單個磚塊寬（透過 width_multiplier 調整）
    - 跟隨滑鼠的 x 座標移動，y 固定在視窗底部上方
    - 不會超出視窗邊界
    """

    def __init__(
        self,
        brick_obj,
        width_multiplier=2.5,
        height=14,
        y_offset=40,
        color=(220, 220, 220),
        screen_width=800,
        screen_height=600,
    ):
        # 以 Brick 的 brick_width 當基準，確保比磚塊寬
        self.brick_width = brick_obj.brick_width
        self.width = int(self.brick_width * width_multiplier)
        self.height = height
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 初始置中顯示，y 固定在底部上方
        start_x = (self.screen_width - self.width) // 2
        self.y = self.screen_height - y_offset
        self.rect = pygame.Rect(start_x, self.y, self.width, self.height)

    def update(self):
        # 取得滑鼠座標，把 paddle 中心移到滑鼠 x，並夾在視窗內
        mx, _ = pygame.mouse.get_pos()
        new_x = mx - self.width // 2
        # clamp
        new_x = max(0, min(new_x, self.screen_width - self.width))
        self.rect.x = new_x

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Ball:
    """球物件，負責在遊戲中移動並進行碰撞偵測。

    屬性:
    - 大小（半徑）
    - 顏色
    - 初始位置（x, y）
    - 速度（x_speed, y_speed）
    - 是否已發球（started）
    """

    def __init__(
        self,
        x=400,
        y=500,
        radius=8,
        color=(255, 255, 255),
        x_speed=5,
        y_speed=-5,
        screen_width=800,
        screen_height=600,
        started=False,
    ):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.started = started  # 是否已開始發球

        # 建立碰撞檢測用的矩形區域
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)

    def move(self):
        """移動球的位置"""
        if self.started:
            self.x += self.x_speed
            self.y += self.y_speed

            # 更新碰撞檢測矩形
            self.rect.centerx = self.x
            self.rect.centery = self.y

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

        # 上邊界碰撞
        if self.y - self.radius <= 0:
            self.y_speed = -self.y_speed
            self.y = self.radius

    def check_paddle_collision(self, paddle):
        """檢查球與底板的碰撞"""
        if self.rect.colliderect(paddle.rect) and self.y_speed > 0:
            # 計算球撞擊底板的相對位置（-1到1）
            hit_pos = (self.x - paddle.rect.centerx) / (paddle.width / 2)

            # 根據撞擊位置改變球的水平速度
            self.x_speed = hit_pos * abs(self.y_speed)
            self.y_speed = -abs(self.y_speed)

            # 確保球不會卡在底板裡
            self.y = paddle.rect.top - self.radius

    def check_brick_collision(self, brick_wall):
        """檢查球與磚塊的碰撞"""
        for brick in brick_wall.bricks:
            if not brick["is_hit"] and self.rect.colliderect(brick["rect"]):
                # 標記磚塊已被擊中
                brick["is_hit"] = True

                # 判斷碰撞方向並反彈
                brick_center_x = brick["rect"].centerx
                brick_center_y = brick["rect"].centery

                # 計算球心與磚塊中心的距離
                dx = abs(self.x - brick_center_x)
                dy = abs(self.y - brick_center_y)

                # 根據碰撞位置決定反彈方向
                if dx / (brick["rect"].width / 2) > dy / (brick["rect"].height / 2):
                    # 左右邊碰撞
                    self.x_speed = -self.x_speed
                else:
                    # 上下邊碰撞
                    self.y_speed = -self.y_speed

                return True  # 有碰撞發生
        return False  # 沒有碰撞

    def is_out_of_bounds(self):
        """檢查球是否掉出螢幕下方"""
        return self.y - self.radius > self.screen_height

    def follow_paddle(self, paddle):
        """讓球跟隨底板移動（僅在球尚未發射時）"""
        if not self.started:
            # 讓球的x座標與底板中心對齊
            self.x = paddle.rect.centerx
            # 保持球在底板上方固定距離
            self.y = paddle.rect.top - self.radius - 5  # 距離底板上方5像素

            # 更新碰撞檢測矩形
            self.rect.centerx = self.x
            self.rect.centery = self.y

    def start(self):
        """開始發球"""
        self.started = True

    def reset(self, x=400, y=500):
        """重置球的位置和狀態"""
        self.x = x
        self.y = y
        self.started = False
        self.rect.centerx = x
        self.rect.centery = y

    def draw(self, screen):
        """繪製球"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


######################定義函式區######################

######################初始化設定######################
pygame.init()  # 啟動pygame
clock = pygame.time.Clock()  # 建立時鐘物件
width = 800  # 設定視窗寬度
height = 600  # 設定視窗高度

######################載入圖片######################

######################遊戲視窗設定######################
# 設定視窗大小
screen = pygame.display.set_mode((width, height))
# 設定視窗標題
pygame.display.set_caption("敲磚塊遊戲")

######################磚塊######################
# 建立 10x5 磚牆並置中
# Brick 物件現在代表整面磚牆（cols, rows, brick_width, brick_height, padding, top_margin, screen_width）
brick_wall = Brick(
    cols=10,
    rows=5,
    brick_width=60,
    brick_height=20,
    padding=6,
    top_margin=50,
    screen_width=width,
)

# 建立玩家可操控的底板，寬度以磚塊為基準放大
paddle = Paddle(
    brick_wall,
    width_multiplier=2.5,
    height=14,
    y_offset=40,
    screen_width=width,
    screen_height=height,
)


######################顯示文字設定######################
# 嘗試載入支援繁體中文的字體，若找不到則使用預設字體
def load_chinese_font(size):
    # 常見的繁體中文字體名稱，依序嘗試
    candidates = [
        "Microsoft JhengHei",
        "Microsoft JhengHei UI",
        "Noto Sans CJK TC",
        "PingFang TC",
        "Arial Unicode MS",
    ]
    for name in candidates:
        try:
            path = pygame.font.match_font(name)
        except Exception:
            path = None
        if path:
            return pygame.font.Font(path, size)

    # 若以上都找不到，回退到系統預設字體
    return pygame.font.SysFont(None, size)


# 分數與字體設定
score = 0
score_font = load_chinese_font(28)
info_font = load_chinese_font(16)
text_padding = 10  # 從視窗邊緣的距離

######################底板設定######################

######################球設定######################
# 創建球物件
ball = Ball(
    x=width // 2,  # 初始位置在螢幕中央
    y=height - 60,  # 在底板上方適當位置
    radius=8,
    color=(255, 255, 255),  # 白色球
    x_speed=7,  # 加快水平速度
    y_speed=-7,  # 加快垂直速度
    screen_width=width,
    screen_height=height,
    started=False,  # 初始狀態未發球
)

######################遊戲結束設定######################

######################主程式######################
# 遊戲主迴圈
while True:
    # fps = 60
    # 讓遊戲迴圈執行速度固定在每秒 60 次
    clock.tick(60)

    # 偵測事件
    for event in pygame.event.get():
        # 使用者按關閉按鈕
        if event.type == pygame.QUIT:  # 如果按下[X]就退出
            sys.exit()  # 離開遊戲

        # 滑鼠點擊事件 - 發球
        if event.type == pygame.MOUSEBUTTONDOWN and not ball.started:
            ball.start()  # 開始發球

        # 鍵盤事件 - 空白鍵發球
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not ball.started:
                ball.start()  # 開始發球

    # 更新遊戲物件
    paddle.update()

    # 如果球尚未發射，讓球跟隨底板移動
    ball.follow_paddle(paddle)

    # 更新球的位置
    ball.move()

    # 檢查球是否掉出下邊界，如果是則自動重置
    if ball.is_out_of_bounds():
        # 重置球到底板中心上方
        ball.reset(paddle.rect.centerx, paddle.rect.top - ball.radius - 5)

    # 檢查球的碰撞
    ball.check_wall_collision()
    ball.check_paddle_collision(paddle)
    # 若有擊中磚塊，增加分數（每塊 10 分）
    if ball.check_brick_collision(brick_wall):
        score += 10

    # 填充背景色
    screen.fill((0, 0, 0))  # 黑色背景

    # 繪製磚牆
    brick_wall.draw(screen)

    # 繪製底板
    paddle.draw(screen)

    # 繪製球
    ball.draw(screen)

    # 繪製右上角的分數與提示文字（繁體中文）
    score_text = f"分數: {score}"
    score_surf = score_font.render(score_text, True, (255, 255, 255))
    score_rect = score_surf.get_rect(topright=(width - text_padding, text_padding))
    screen.blit(score_surf, score_rect)

    info_text = "滑鼠點擊發球"
    info_surf = info_font.render(info_text, True, (200, 200, 200))
    info_rect = info_surf.get_rect(
        topright=(width - text_padding, score_rect.bottom + 6)
    )
    screen.blit(info_surf, info_rect)

    # 更新視窗
    pygame.display.update()
