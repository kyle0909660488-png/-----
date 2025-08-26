"""
敲磚塊遊戲主程式
使用重新整理過的模組化架構
"""

import sys
import os

# 將專案根目錄加入 Python 路徑，確保能正確 import 模組
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 匯入必要模組
import config.settings as config
from src.game import GameEngine


def main():
    """遊戲主函式"""
    try:
        # 建立遊戲引擎
        game = GameEngine(config)

        # 啟動遊戲
        game.run()

    except KeyboardInterrupt:
        print("遊戲被使用者中斷")
    except Exception as e:
        print(f"遊戲發生錯誤：{e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
