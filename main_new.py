######################載入套件######################
"""
敲磚塊遊戲主程式 - 模組化架構版本\n
\n
此版本使用重新整理過的模組化架構，將遊戲邏輯拆分為：\n
- config/settings.py: 集中式設定檔\n
- src/game/: 遊戲核心邏輯\n
- src/game_objects/: 獨立遊戲物件類別\n
- src/utils/: 工具函式和繁體中文支援\n
\n
執行方式：python main_new.py\n
"""
import sys
import os

######################初始化設定######################
# 將專案根目錄加入 Python 路徑，確保能正確 import 模組
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 匯入必要模組
import config.settings as config
from src.game import GameEngine


######################定義函式區######################
def main():
    """
    遊戲主函式 - 負責啟動和管理整個遊戲流程\n
    \n
    此函式執行以下操作：\n
    1. 建立遊戲引擎物件\n
    2. 啟動遊戲主迴圈\n
    3. 處理異常狀況（使用者中斷、程式錯誤）\n
    \n
    異常處理：\n
    - KeyboardInterrupt: 使用者按 Ctrl+C 中斷遊戲\n
    - 其他例外: 顯示錯誤訊息並印出完整錯誤堆疊\n
    """
    try:
        # 建立遊戲引擎，傳入設定模組
        game = GameEngine(config)

        # 啟動遊戲主迴圈，開始執行遊戲
        game.run()

    except KeyboardInterrupt:
        # 使用者按 Ctrl+C 中斷遊戲時的處理
        print("遊戲被使用者中斷")
    except Exception as e:
        # 其他錯誤發生時的處理
        print(f"遊戲發生錯誤：{e}")
        import traceback

        # 印出完整的錯誤堆疊，方便除錯
        traceback.print_exc()


######################主程式######################
# 直接執行主函式，不使用 if __name__ == "__main__": 慣例
main()
