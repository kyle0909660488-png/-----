# 敲磚塊遊戲 AI 編程指引

## 項目架構

這是一個 Pygame 敲磚塊遊戲，採用**模組化架構**，分為配置層、遊戲邏輯層、遊戲物件層和工具層：

```
config/settings.py    # 集中式設定檔（所有常數）
src/game/             # 遊戲核心邏輯
src/game_objects/     # 獨立遊戲物件類別
src/utils/            # 繁體中文支援和工具函式
```

### 核心設計模式

- **組合模式**：`GameEngine` 組合所有遊戲物件，避免繼承複雜度
- **集中式設定**：所有參數在 `config/settings.py`，修改平衡性不需動程式邏輯
- **狀態管理**：使用 `GameStateManager` 處理遊戲狀態轉換
- **繁體中文支援**：通過 `font_loader.py` 自動偵測系統字型

## 開發工作流程

### 執行遊戲

```powershell
# 新版模組化架構（推薦）
python main_new.py

# 舊版單檔版本
python main.py
```

### 環境設定

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 項目特定慣例

### 1. 設定管理

- **所有常數** 放在 `config/settings.py`，不在程式碼中硬編碼
- 顏色使用 `src/utils/colors.py` 的命名常數
- 字型大小、間距、速度等都可在設定檔調整

### 2. 遊戲物件設計

每個遊戲物件類別（Ball、Paddle、Brick）遵循：

- **獨立性**：可單獨測試和重用
- **配置驅動**：接受配置參數，不依賴全域變數
- **職責單一**：Ball 只管移動和碰撞，Paddle 只管控制和縮放

### 3. 繁體中文處理

```python
# 使用工具函式載入中文字型
from src.utils.font_loader import load_chinese_font
font = load_chinese_font(24)

# 字型候選清單在 settings.py 中定義
CHINESE_FONT_CANDIDATES = ["Microsoft JhengHei", ...]
```

### 4. 碰撞檢測慣例

- Brick 使用方向性碰撞檢測（horizontal/vertical）影響球反彈
- Paddle 碰撞根據撞擊位置改變球的反彈角度
- 特殊磚塊爆炸使用 3x3 範圍檢測

## 特殊功能實現

### 特殊磚塊系統

- 在 `Brick.__init__` 中隨機選擇特殊磚塊
- 使用時間戳記實現閃爍效果：`pygame.time.get_ticks()`
- 爆炸邏輯在 `_explode_around` 方法中處理 3x3 範圍

### 動態底板縮小

- 每次擊中磚塊後呼叫 `paddle.shrink()`
- 使用 `max(min_width, current_width - shrink_amount)` 確保不會過小
- 縮小時重新居中以保持遊戲平衡

### 遊戲狀態管理

```python
# 狀態轉換邏輯
GameState.WAITING_TO_START -> GameState.PLAYING -> GameState.WIN
# 使用 GameStateManager 統一管理狀態和分數
```

## 檔案修改指引

### 調整遊戲平衡

1. 修改 `config/settings.py` 中的數值
2. 球速：`BALL_SPEED_X/Y`
3. 底板縮小：`PADDLE_SHRINK_AMOUNT`
4. 特殊磚塊數量：`SPECIAL_BRICK_COUNT`

### 新增遊戲功能

1. **新遊戲物件**：在 `src/game_objects/` 建立新類別
2. **新工具函式**：在 `src/utils/` 建立對應模組
3. **整合到引擎**：在 `GameEngine` 中組合新物件

### 除錯和測試

- 使用 `python -u` 確保即時輸出
- 遊戲物件可獨立匯入測試
- 修改設定檔可快速驗證平衡性調整

## 常見陷阱

- **字型載入失敗**：確保系統有繁體中文字型，或在 `CHINESE_FONT_CANDIDATES` 中新增候選
- **座標計算**：pygame 座標系原點在左上角，y 軸向下
- **狀態管理**：確保狀態轉換邏輯正確，避免球在錯誤狀態下移動
- **模組匯入**：注意 `main_new.py` 中的路徑設定，確保模組正確載入
