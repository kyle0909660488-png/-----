"""
遊戲設定檔案
包含所有遊戲的設定參數和常數
"""

# 視窗設定
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "敲磚塊遊戲"
FPS = 60

# 顏色設定 (RGB)
BACKGROUND_COLOR = (0, 0, 0)  # 黑色背景
TEXT_COLOR = (255, 255, 255)  # 白色文字
INFO_TEXT_COLOR = (200, 200, 200)  # 灰色資訊文字

# 磚塊設定
BRICK_COLS = 10
BRICK_ROWS = 5
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
BRICK_PADDING = 6
BRICK_TOP_MARGIN = 50
SPECIAL_BRICK_COUNT = 7  # 特殊爆炸磚塊數量

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

# 底板設定
PADDLE_WIDTH_MULTIPLIER = 2.5
PADDLE_HEIGHT = 14
PADDLE_Y_OFFSET = 40
PADDLE_COLOR = (220, 220, 220)
PADDLE_SHRINK_AMOUNT = 5  # 每次擊中磚塊後底板縮小的像素數
PADDLE_MIN_WIDTH = 40  # 底板最小寬度

# 球設定
BALL_RADIUS = 8
BALL_COLOR = (255, 255, 255)
BALL_SPEED_X = 7
BALL_SPEED_Y = -7
BALL_FOLLOW_DISTANCE = 5  # 球跟隨底板時的距離

# 遊戲設定
SCORE_PER_BRICK = 10
TEXT_PADDING = 10

# 字體設定
SCORE_FONT_SIZE = 28
INFO_FONT_SIZE = 16
WIN_FONT_SIZE = 48

# 特殊效果設定
SPECIAL_BRICK_FLASH_INTERVAL = 300  # 特殊磚塊閃爍間隔 (毫秒)
SPECIAL_BRICK_OUTLINE_COLORS = [(255, 69, 0), (255, 215, 0)]  # 閃爍顏色

# 繁體中文字體候選清單
CHINESE_FONT_CANDIDATES = [
    "Microsoft JhengHei",
    "Microsoft JhengHei UI",
    "Noto Sans CJK TC",
    "PingFang TC",
    "Arial Unicode MS",
]
