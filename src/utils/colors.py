"""
顏色常數定義模組
提供遊戲中使用的各種顏色常數
"""

# 基本顏色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 灰階顏色
LIGHT_GRAY = (200, 200, 200)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# 遊戲專用顏色
BACKGROUND_COLOR = BLACK
TEXT_COLOR = WHITE
INFO_TEXT_COLOR = LIGHT_GRAY
PADDLE_COLOR = LIGHT_GRAY
BALL_COLOR = WHITE

# 磚塊顏色調色盤
BRICK_COLORS = [
    (255, 99, 71),  # 番茄紅
    (255, 165, 0),  # 橙色
    (255, 215, 0),  # 金色
    (144, 238, 144),  # 淺綠色
    (135, 206, 250),  # 天空藍
    (216, 191, 216),  # 薊色
    (173, 216, 230),  # 淺藍色
    (240, 128, 128),  # 淺珊瑚色
    (255, 182, 193),  # 淺粉色
    (152, 251, 152),  # 淺春綠色
]

# 特殊效果顏色
SPECIAL_BRICK_FLASH_COLORS = [(255, 69, 0), (255, 215, 0)]


def get_text_color_for_background(bg_color):
    """根據背景顏色決定合適的文字顏色（深色背景用白字，淺色背景用黑字）"""
    r, g, b = bg_color
    brightness = (r + g + b) / 3
    return WHITE if brightness < 140 else BLACK
