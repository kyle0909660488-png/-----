######################載入套件######################
import pygame
import sys
import random


######################物件類別######################
class Brick:
    """
    磚塊牆類別 - 管理整面磚塊的生成、繪製和碰撞檢測\n
    \n
    此類別負責建立一整面由多行多列組成的磚牆，每個磚塊都有：\n
    - 獨立的位置和尺寸\n
    - 不同的顏色（按欄位區分）\n
    - 擊中狀態追蹤\n
    - 特殊爆炸磚塊標記\n
    \n
    特殊功能：\n
    - 自動計算磚牆置中位置\n
    - 隨機生成特殊爆炸磚塊\n
    - 爆炸磚塊會摧毀周圍 3x3 範圍的磚塊\n
    - 閃爍效果提示特殊磚塊\n
    """

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
        """
        建立磚塊牆物件\n
        \n
        參數:\n
        cols (int): 磚塊欄數，建議範圍 8-12\n
        rows (int): 磚塊列數，建議範圍 3-8\n
        brick_width (int): 單個磚塊寬度，單位像素\n
        brick_height (int): 單個磚塊高度，單位像素\n
        padding (int): 磚塊間距，單位像素\n
        top_margin (int): 磚牆距離螢幕上方的距離\n
        screen_width (int): 螢幕寬度，用於計算磚牆置中位置\n
        \n
        建立過程：\n
        1. 計算磚牆總寬度並置中\n
        2. 逐行逐列建立磚塊資料\n
        3. 為每個磚塊分配顏色（按欄位循環）\n
        4. 隨機選擇特殊爆炸磚塊\n
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
        color_palette = [
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
        # 我們也會記錄 row/col 以利爆炸擴散判斷，並標記部分為特殊磚塊
        self.bricks = []
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (brick_width + padding)
                y = top_margin + row * (brick_height + padding)
                # 每個磚塊使用 color_palette 中不同的顏色（以 column 為主），若不足則循環
                color = color_palette[col % len(color_palette)]
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

        # 每局隨機挑選最多 7 個特殊磚塊（若磚塊總數小於 7，則全部可能被選中）
        special_count = min(7, len(self.bricks))
        special_brick_indices = random.sample(range(len(self.bricks)), k=special_count)
        for idx in special_brick_indices:
            self.bricks[idx]["is_special"] = True

    def draw(self, screen):
        """
        繪製磚塊牆的視覺效果\n
        \n
        此方法會遍歷所有磚塊，只繪製尚未被擊中的磚塊。\n
        特殊磚塊會有額外的視覺效果：\n
        1. 閃爍的彩色外框（每 300ms 切換顏色）\n
        2. 中央顯示中文字「爆」標示其功能\n
        3. 根據磚塊背景顏色自動選擇文字顏色\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件，用於繪製\n
        \n
        繪製順序:\n
        1. 磚塊本體（填滿矩形）\n
        2. 特殊磚塊外框（閃爍效果）\n
        3. 特殊磚塊文字標示\n
        """
        # 遍歷所有磚塊，只畫還沒被打破的
        for brick_item in self.bricks:
            if not brick_item["is_hit"]:
                # 繪製磚塊本體
                pygame.draw.rect(screen, brick_item["color"], brick_item["rect"])

                # 若為特殊磚塊，使用更明顯且易辨識的標示：
                # - 會閃爍的外框（每 300ms 切換顏色）
                # - 在磚塊中央顯示中文字『爆』以明確傳達功能
                if brick_item.get("is_special", False):
                    # 閃爍效果（以時間分段切換顏色）
                    current_tick = pygame.time.get_ticks()
                    flash_phase = (current_tick // 300) % 2  # 每 300 毫秒切換一次
                    outline_color = (255, 69, 0) if flash_phase == 0 else (255, 215, 0)

                    # 畫較粗的外框讓玩家容易注意到
                    pygame.draw.rect(screen, outline_color, brick_item["rect"], 3)

                    # 嘗試畫中文字 "爆" 在磚塊中央（使用專用的中文字型載入器）
                    try:
                        # 選擇合適大小，確保在磚塊內可見
                        font_size = max(
                            12, int(min(brick_item["rect"].height * 0.9, 24))
                        )
                        font = load_chinese_font(font_size)

                        # 根據磚塊顏色決定文字顏色（深色磚塊用白字，淺色用黑字）
                        brick_red, brick_green, brick_blue = brick_item["color"]
                        brightness = (brick_red + brick_green + brick_blue) / 3
                        text_color = (255, 255, 255) if brightness < 140 else (0, 0, 0)

                        # 渲染文字並置中顯示
                        text_surf = font.render("爆", True, text_color)
                        text_rect = text_surf.get_rect(center=brick_item["rect"].center)
                        screen.blit(text_surf, text_rect)
                    except Exception:
                        # 若字型或繪製失敗，保留外框作為標示
                        pass


class Paddle:
    """
    玩家操控的底板類別 - 負責接球和反彈控制\n
    \n
    底板的行為特性：\n
    - 寬度以磚塊寬度為基準，可透過倍數調整\n
    - 跟隨滑鼠的 x 座標移動，y 位置固定在視窗底部\n
    - 不會移動到視窗邊界之外\n
    - 每次擊中磚塊後會縮小一定像素，增加遊戲難度\n
    - 有最小寬度限制，避免底板過小無法操作\n
    \n
    碰撞機制：\n
    - 球撞擊不同位置會產生不同的反彈角度\n
    - 撞擊中央：垂直反彈\n
    - 撞擊邊緣：斜向反彈，角度更大\n
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
        """
        初始化底板物件\n
        \n
        參數:\n
        brick_obj (Brick): 磚塊物件，用來取得磚塊寬度作為底板寬度基準\n
        width_multiplier (float): 寬度倍數，底板寬度 = 磚塊寬度 × 此倍數，範圍建議 2.0-4.0\n
        height (int): 底板高度，單位像素，建議範圍 10-20\n
        y_offset (int): 距離螢幕底部的距離，單位像素\n
        color (tuple): 底板顏色，RGB 格式 (r, g, b)，範圍 0-255\n
        screen_width (int): 螢幕寬度，用於邊界限制\n
        screen_height (int): 螢幕高度，用於計算底板 y 位置\n
        \n
        初始化過程:\n
        1. 以磚塊寬度為基準計算底板寬度\n
        2. 將底板置中於螢幕下方\n
        3. 建立碰撞檢測矩形\n
        """
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
        """
        更新底板位置 - 讓底板跟隨滑鼠移動\n
        \n
        此方法執行以下操作：\n
        1. 取得目前滑鼠的 x 座標\n
        2. 計算底板中心應該移到的位置\n
        3. 限制底板不超出螢幕左右邊界\n
        4. 更新底板的碰撞矩形位置\n
        \n
        邊界處理：\n
        - 左邊界：底板左邊不會超出 x=0\n
        - 右邊界：底板右邊不會超出螢幕寬度\n
        """
        # 取得滑鼠座標，把 paddle 中心移到滑鼠 x，並夾在視窗內
        mouse_x, _ = pygame.mouse.get_pos()
        # 計算底板左上角應該在的位置（讓底板中心對準滑鼠）
        new_x = mouse_x - self.width // 2
        # 限制在螢幕範圍內（clamp 操作）
        new_x = max(0, min(new_x, self.screen_width - self.width))
        # 更新底板位置
        self.rect.x = new_x

    def draw(self, screen):
        """
        繪製底板到螢幕上\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        \n
        繪製方式：\n
        使用純色填滿矩形來表示底板\n
        """
        # 用設定的顏色畫出底板矩形
        pygame.draw.rect(screen, self.color, self.rect)


class Ball:
    """
    球物件類別 - 遊戲中的主要運動物體\n
    \n
    球的行為特性：\n
    - 在螢幕內以固定速度直線移動\n
    - 碰到邊界會反彈（左右上邊界）\n
    - 撞到底板會根據撞擊位置改變反彈角度\n
    - 撞到磚塊會反彈並摧毀磚塊\n
    - 掉到螢幕底部會重新開始\n
    \n
    狀態管理：\n
    - started: False 時球會跟隨底板移動\n
    - started: True 時球開始自由移動\n
    \n
    物理特性：\n
    - 速度向量 (x_speed, y_speed)\n
    - 半徑碰撞檢測\n
    - 邊界彈性碰撞\n
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
        """
        初始化球物件\n
        \n
        參數:\n
        x (int): 初始 x 座標，螢幕座標系統\n
        y (int): 初始 y 座標，螢幕座標系統\n
        radius (int): 球的半徑，單位像素，建議範圍 5-15\n
        color (tuple): 球的顏色，RGB 格式 (r, g, b)，範圍 0-255\n
        x_speed (int): 水平移動速度，正值向右，負值向左，建議範圍 3-10\n
        y_speed (int): 垂直移動速度，正值向下，負值向上，建議範圍 3-10\n
        screen_width (int): 螢幕寬度，用於邊界碰撞檢測\n
        screen_height (int): 螢幕高度，用於邊界碰撞檢測\n
        started (bool): 是否已開始移動，False 時會跟隨底板\n
        \n
        初始化項目：\n
        1. 設定球的位置和外觀屬性\n
        2. 設定移動速度向量\n
        3. 建立碰撞檢測用的矩形區域\n
        """
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
        """
        移動球的位置 - 根據速度向量更新球的座標\n
        \n
        移動條件：\n
        - 只有當 started=True 時球才會移動\n
        - started=False 時球保持靜止（跟隨底板）\n
        \n
        移動計算：\n
        - 新 x 座標 = 目前 x + x 方向速度\n
        - 新 y 座標 = 目前 y + y 方向速度\n
        - 同時更新碰撞檢測矩形的位置\n
        """
        if self.started:
            # 根據速度移動球的位置
            self.x += self.x_speed
            self.y += self.y_speed

            # 更新碰撞檢測矩形
            self.rect.centerx = self.x
            self.rect.centery = self.y

    def check_wall_collision(self):
        """
        檢查球與視窗邊界的碰撞 - 處理左右上邊界反彈\n
        \n
        碰撞檢測：\n
        1. 左右邊界：球的邊緣觸及螢幕左右邊界時反彈\n
        2. 上邊界：球的頂部觸及螢幕上方時向下反彈\n
        3. 下邊界：不在此處理（由主程式處理掉球重置）\n
        \n
        反彈處理：\n
        - 水平碰撞：x_speed 變為相反值\n
        - 垂直碰撞：y_speed 變為相反值\n
        - 防卡牆機制：將球移回邊界內\n
        """
        # 左右邊界碰撞檢測和處理
        if self.x - self.radius <= 0 or self.x + self.radius >= self.screen_width:
            # 水平方向速度反轉
            self.x_speed = -self.x_speed
            # 防止球卡在邊界外（修正位置）
            if self.x - self.radius <= 0:
                self.x = self.radius  # 移到左邊界內側
            else:
                self.x = self.screen_width - self.radius  # 移到右邊界內側

        # 上邊界碰撞檢測和處理
        if self.y - self.radius <= 0:
            # 垂直方向速度反轉（向下彈）
            self.y_speed = -self.y_speed
            # 修正位置避免卡在邊界外
            self.y = self.radius

    def check_paddle_collision(self, paddle):
        """
        檢查球與底板的碰撞 - 實現角度反彈機制\n
        \n
        碰撞條件：\n
        1. 球的碰撞矩形與底板矩形重疊\n
        2. 球正在向下移動（y_speed > 0）\n
        \n
        角度計算：\n
        - 撞擊位置 = (球x - 底板中心x) / (底板寬度/2)\n
        - 撞擊位置範圍：-1（最左邊）到 1（最右邊）\n
        - 水平速度 = 撞擊位置 × 垂直速度的絕對值\n
        \n
        反彈效果：\n
        - 撞擊中央：垂直反彈\n
        - 撞擊邊緣：斜向反彈，角度更大\n
        - 防卡機制：確保球在底板上方\n
        \n
        參數:\n
        paddle (Paddle): 底板物件\n
        """
        if self.rect.colliderect(paddle.rect) and self.y_speed > 0:
            # 計算球撞擊底板的相對位置（-1到1）
            hit_position = (self.x - paddle.rect.centerx) / (paddle.width / 2)

            # 根據撞擊位置改變球的水平速度
            # 撞到邊邊會彈得比較斜，撞到中間比較垂直
            self.x_speed = hit_position * abs(self.y_speed)
            # 垂直速度改為向上（絕對值保持，方向相反）
            self.y_speed = -abs(self.y_speed)

            # 確保球不會卡在底板裡（移到底板上方）
            self.y = paddle.rect.top - self.radius

    def check_brick_collision(self, brick_wall, paddle=None, shrink_by=5):
        """
        檢查球與磚塊的碰撞 - 處理磚塊破壞和底板縮小\n
        \n
        碰撞檢測過程：\n
        1. 遍歷所有未被擊中的磚塊\n
        2. 檢查球的矩形是否與磚塊矩形重疊\n
        3. 標記被撞擊的磚塊為已擊中\n
        4. 如果是特殊磚塊，觸發爆炸效果\n
        5. 計算反彈方向並改變球的速度\n
        6. 縮小底板寬度\n
        \n
        爆炸機制：\n
        - 特殊磚塊被擊中時會摧毀周圍 3×3 範圍的磚塊\n
        - 爆炸範圍：上下左右各延伸 1 格\n
        \n
        反彈方向判斷：\n
        - 比較球心與磚塊中心的 x、y 距離\n
        - 水平距離較大：水平反彈\n
        - 垂直距離較大：垂直反彈\n
        \n
        參數:\n
        brick_wall (Brick): 磚塊牆物件\n
        paddle (Paddle): 底板物件，用於縮小處理\n
        shrink_by (int): 底板每次縮小的像素數\n
        \n
        回傳:\n
        int: 被擊中的磚塊數量（包含爆炸連帶摧毀的）\n
        """
        # 遍歷所有磚塊，檢查碰撞
        for brick_index, brick in enumerate(brick_wall.bricks):
            if not brick["is_hit"] and self.rect.colliderect(brick["rect"]):
                # 先標記這顆磚塊已被擊中
                brick["is_hit"] = True
                hit_count = 1

                # 若為特殊磚塊，則炸掉周圍 8 格（包含自己已標記）
                if brick.get("is_special", False):
                    brick_row = brick["row"]
                    brick_col = brick["col"]
                    # 檢查周圍 3x3 範圍的磚塊
                    for other_brick in brick_wall.bricks:
                        if not other_brick["is_hit"]:
                            # 計算距離，如果在爆炸範圍內就摧毀
                            if (
                                abs(other_brick["row"] - brick_row) <= 1
                                and abs(other_brick["col"] - brick_col) <= 1
                            ):
                                other_brick["is_hit"] = True
                                hit_count += 1

                # 判斷碰撞方向並反彈（以原本磚塊中心判斷）
                brick_center_x = brick["rect"].centerx
                brick_center_y = brick["rect"].centery

                # 計算球心與磚塊中心的距離
                distance_x = abs(self.x - brick_center_x)
                distance_y = abs(self.y - brick_center_y)

                # 根據距離比例判斷主要碰撞方向
                if distance_x / (brick["rect"].width / 2) > distance_y / (
                    brick["rect"].height / 2
                ):
                    # 水平碰撞：左右反彈
                    self.x_speed = -self.x_speed
                else:
                    # 垂直碰撞：上下反彈
                    self.y_speed = -self.y_speed

                # 如果有傳入 paddle，則在每次擊中（事件）時縮小底板寬度一次
                if paddle is not None:
                    try:
                        # 記住底板中心位置
                        old_center_x = paddle.rect.centerx
                        # 計算新寬度，但不能小於最小寬度
                        new_width = max(40, int(paddle.width - shrink_by))
                        # 更新底板寬度和矩形
                        paddle.width = new_width
                        paddle.rect.width = new_width
                        # 保持底板中心位置不變
                        paddle.rect.centerx = old_center_x
                        # 確保底板不會超出螢幕邊界
                        paddle.rect.x = max(
                            0, min(paddle.rect.x, paddle.screen_width - paddle.width)
                        )
                    except Exception:
                        # 如果底板縮小過程出錯，忽略此次縮小
                        pass

                return hit_count

        return 0

    def is_out_of_bounds(self):
        """
        檢查球是否掉出螢幕下方\n
        \n
        回傳:\n
        bool: True 表示球已掉出下邊界，需要重置\n
        """
        return self.y - self.radius > self.screen_height

    def follow_paddle(self, paddle):
        """
        讓球跟隨底板移動 - 僅在球尚未發射時有效\n
        \n
        跟隨機制：\n
        1. 球的 x 座標與底板中心對齊\n
        2. 球保持在底板上方固定距離（5像素）\n
        3. 同時更新碰撞檢測矩形位置\n
        \n
        使用時機：\n
        - 遊戲開始時\n
        - 球掉出邊界重置後\n
        - 任何 started=False 的情況\n
        \n
        參數:\n
        paddle (Paddle): 要跟隨的底板物件\n
        """
        if not self.started:
            # 讓球的x座標與底板中心對齊
            self.x = paddle.rect.centerx
            # 保持球在底板上方固定距離
            self.y = paddle.rect.top - self.radius - 5  # 距離底板上方5像素

            # 更新碰撞檢測矩形
            self.rect.centerx = self.x
            self.rect.centery = self.y

    def start(self):
        """
        開始發球 - 讓球從跟隨狀態轉為自由移動狀態\n
        """
        self.started = True

    def reset(self, x=400, y=500):
        """
        重置球的位置和狀態 - 回到初始狀態\n
        \n
        重置項目：\n
        1. 球的位置座標\n
        2. 移動狀態（started = False）\n
        3. 碰撞檢測矩形位置\n
        \n
        參數:\n
        x (int): 重置後的 x 座標\n
        y (int): 重置後的 y 座標\n
        """
        self.x = x
        self.y = y
        self.started = False  # 回到跟隨底板狀態
        self.rect.centerx = x
        self.rect.centery = y

    def draw(self, screen):
        """
        繪製球到螢幕上\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        \n
        繪製方式：\n
        使用 pygame.draw.circle 繪製實心圓形\n
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


######################定義函式區######################
def load_chinese_font(size):
    """
    載入支援繁體中文的字體，若找不到則使用預設字體\n
    \n
    此函數會依序嘗試載入系統中常見的繁體中文字型，\n
    若都找不到則回退到系統預設字型。\n
    \n
    參數:\n
    size (int): 字體大小，建議範圍 12-48\n
    \n
    回傳:\n
    pygame.font.Font: 字型物件，可用於繪製文字\n
    \n
    載入順序:\n
    1. Microsoft JhengHei（Windows 系統預設）\n
    2. Microsoft JhengHei UI（Windows 10+）\n
    3. Noto Sans CJK TC（跨平台開源字型）\n
    4. PingFang TC（macOS 系統）\n
    5. Arial Unicode MS（舊版萬國碼字型）\n
    6. 系統預設字型（最後備案）\n
    """
    # 常見的繁體中文字體名稱，依序嘗試
    font_candidates = [
        "Microsoft JhengHei",
        "Microsoft JhengHei UI",
        "Noto Sans CJK TC",
        "PingFang TC",
        "Arial Unicode MS",
    ]
    # 依序檢查每個字型是否存在於系統中
    for font_name in font_candidates:
        try:
            # 嘗試找到字型檔案路徑
            font_path = pygame.font.match_font(font_name)
        except Exception:
            # 如果找不到就跳過這個字型
            font_path = None
        if font_path:
            # 找到字型就回傳載入的字型物件
            return pygame.font.Font(font_path, size)

    # 若以上都找不到，回退到系統預設字體
    return pygame.font.SysFont(None, size)


######################初始化設定######################
pygame.init()  # 啟動 pygame 遊戲引擎
game_clock = pygame.time.Clock()  # 建立時鐘物件，用於控制遊戲幀率
screen_width = 800  # 設定視窗寬度（像素）
screen_height = 600  # 設定視窗高度（像素）
FPS = 60  # 遊戲幀率常數

######################載入圖片######################

######################遊戲視窗設定######################
# 設定視窗大小
screen = pygame.display.set_mode((screen_width, screen_height))
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
    screen_width=screen_width,
)

# 建立玩家可操控的底板，寬度以磚塊為基準放大
paddle = Paddle(
    brick_wall,
    width_multiplier=2.5,
    height=14,
    y_offset=40,
    screen_width=screen_width,
    screen_height=screen_height,
)


######################顯示文字設定######################
# 分數與字體設定
score = 0  # 遊戲分數
score_font = load_chinese_font(28)  # 分數顯示字型
info_font = load_chinese_font(16)  # 資訊文字字型
text_padding = 10  # 文字距離視窗邊緣的距離

# 遊戲狀態設定
is_win = False  # 勝利旗標（當所有磚塊被擊中時為 True）

# 遊戲常數
SCORE_PER_BRICK = 10  # 每個磚塊的分數
PADDLE_SHRINK_AMOUNT = 5  # 底板每次縮小的像素數
MIN_PADDLE_WIDTH = 40  # 底板最小寬度

######################底板設定######################

######################球設定######################
# 創建球物件
ball = Ball(
    x=screen_width // 2,  # 初始位置在螢幕中央
    y=screen_height - 60,  # 在底板上方適當位置
    radius=8,
    color=(255, 255, 255),  # 白色球
    x_speed=7,  # 加快水平速度
    y_speed=-7,  # 加快垂直速度
    screen_width=screen_width,
    screen_height=screen_height,
    started=False,  # 初始狀態未發球
)

######################遊戲結束設定######################

######################主程式######################
# 遊戲主迴圈 - 核心遊戲邏輯執行區域
while True:
    # 控制遊戲執行速度為每秒 60 幀，確保遊戲在不同電腦上運行速度一致
    game_clock.tick(FPS)

    # 事件處理區域 - 處理使用者輸入和系統事件
    for event in pygame.event.get():
        # 使用者按關閉按鈕時退出遊戲
        if event.type == pygame.QUIT:
            sys.exit()  # 立即結束程式

        # 滑鼠點擊事件 - 用於發球
        if event.type == pygame.MOUSEBUTTONDOWN and not ball.started:
            ball.start()  # 讓球開始移動

        # 鍵盤事件處理
        if event.type == pygame.KEYDOWN:
            # 空白鍵發球（與滑鼠點擊功能相同）
            if event.key == pygame.K_SPACE and not ball.started:
                ball.start()

            # 按 E 鍵在勝利後開始下一輪遊戲
            # 檢查多種 E 鍵輸入方式以兼容不同鍵盤佈局
            is_e_pressed = event.key == pygame.K_e or (
                hasattr(event, "unicode")
                and event.unicode
                and event.unicode.lower() == "e"
            )
            if is_e_pressed and is_win:
                # 重新建立所有遊戲物件，開始新一輪
                brick_wall = Brick(
                    cols=10,
                    rows=5,
                    brick_width=60,
                    brick_height=20,
                    padding=6,
                    top_margin=50,
                    screen_width=screen_width,
                )
                paddle = Paddle(
                    brick_wall,
                    width_multiplier=2.5,
                    height=14,
                    y_offset=40,
                    screen_width=screen_width,
                    screen_height=screen_height,
                )
                ball = Ball(
                    x=screen_width // 2,
                    y=screen_height - 60,
                    radius=8,
                    color=(255, 255, 255),
                    x_speed=7,
                    y_speed=-7,
                    screen_width=screen_width,
                    screen_height=screen_height,
                    started=False,
                )
                # 重置遊戲狀態
                score = 0
                is_win = False

    # 遊戲物件更新區域 - 更新所有物件的狀態

    # 更新底板位置（跟隨滑鼠移動）
    paddle.update()

    # 球的狀態更新（根據當前遊戲狀態決定行為）
    if not ball.started and not is_win:
        # 球尚未發射且未勝利時，讓球跟隨底板移動
        ball.follow_paddle(paddle)

    # 移動球的位置（如果球已開始移動）
    ball.move()

    # 邊界檢查和重置處理
    if ball.is_out_of_bounds():
        # 球掉出下邊界時自動重置到底板中心上方
        ball.reset(paddle.rect.centerx, paddle.rect.top - ball.radius - 5)

    # 碰撞檢測區域 - 處理所有碰撞事件

    # 檢查球與牆壁的碰撞（左右上邊界）
    ball.check_wall_collision()

    # 檢查球與底板的碰撞（角度反彈）
    ball.check_paddle_collision(paddle)

    # 檢查球與磚塊的碰撞，並處理分數和底板縮小
    hit_count = ball.check_brick_collision(
        brick_wall, paddle=paddle, shrink_by=PADDLE_SHRINK_AMOUNT
    )
    if hit_count > 0:
        # 每個磚塊給予固定分數，包含爆炸連帶摧毀的磚塊
        score += SCORE_PER_BRICK * hit_count

    # 勝利條件檢查
    remaining_bricks = sum(
        1 for brick_item in brick_wall.bricks if not brick_item["is_hit"]
    )
    if remaining_bricks == 0:
        # 所有磚塊都被擊中，遊戲勝利
        is_win = True
        # 停止球的移動，保持當前位置
        try:
            ball.started = False
        except Exception:
            pass

    # 畫面繪製區域 - 將所有元素繪製到螢幕上

    # 清除上一幀的畫面，填充黑色背景
    screen.fill((0, 0, 0))

    # 繪製遊戲物件（依照繪製順序：背景到前景）
    brick_wall.draw(screen)  # 磚牆
    paddle.draw(screen)  # 底板
    ball.draw(screen)  # 球

    # 繪製使用者介面文字

    # 右上角顯示目前分數
    score_text = f"分數: {score}"
    score_surface = score_font.render(score_text, True, (255, 255, 255))
    score_rect = score_surface.get_rect(
        topright=(screen_width - text_padding, text_padding)
    )
    screen.blit(score_surface, score_rect)

    # 分數下方顯示操作提示
    info_text = "滑鼠點擊發球"
    info_surface = info_font.render(info_text, True, (200, 200, 200))
    info_rect = info_surface.get_rect(
        topright=(screen_width - text_padding, score_rect.bottom + 6)
    )
    screen.blit(info_surface, info_rect)

    # 勝利時顯示特別訊息
    if is_win:
        # 螢幕中央顯示勝利訊息
        win_font = load_chinese_font(48)
        win_surface = win_font.render("你贏了", True, (255, 255, 255))
        win_rect = win_surface.get_rect(
            center=(screen_width // 2, screen_height // 2 - 20)
        )
        screen.blit(win_surface, win_rect)

        # 勝利訊息下方顯示繼續遊戲提示
        next_surface = info_font.render("按 E 開始下一輪", True, (200, 200, 200))
        next_rect = next_surface.get_rect(
            center=(screen_width // 2, screen_height // 2 + 30)
        )
        screen.blit(next_surface, next_rect)

    # 更新整個顯示畫面，讓玩家看到最新的遊戲狀態
    pygame.display.update()
