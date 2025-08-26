"""
字型載入工具模組
提供載入繁體中文字型的功能
"""

import pygame


def load_chinese_font(size, font_candidates=None):
    """
    載入支援繁體中文的字體，若找不到則使用預設字體\n
    size: 字體大小\n
    font_candidates: 字體候選清單，若為 None 則使用預設清單\n
    return: 字體物件\n
    """
    if font_candidates is None:
        font_candidates = [
            "Microsoft JhengHei",
            "Microsoft JhengHei UI",
            "Noto Sans CJK TC",
            "PingFang TC",
            "Arial Unicode MS",
        ]

    # 依序嘗試載入字體
    for font_name in font_candidates:
        try:
            font_path = pygame.font.match_font(font_name)
        except Exception:
            font_path = None
        if font_path:
            return pygame.font.Font(font_path, size)

    # 若以上都找不到，回退到系統預設字體
    return pygame.font.SysFont(None, size)
