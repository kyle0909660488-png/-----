"""
字型載入工具模組
提供載入繁體中文字型的功能
"""

import pygame


def load_chinese_font(size, font_candidates=None):
    """
    載入支援繁體中文的字體，若找不到則使用預設字體

    Args:
        size (int): 字體大小
        font_candidates (list): 字體候選清單，若為 None 則使用預設清單

    Returns:
        pygame.font.Font: 字體物件
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
    for name in font_candidates:
        try:
            path = pygame.font.match_font(name)
        except Exception:
            path = None
        if path:
            return pygame.font.Font(path, size)

    # 若以上都找不到，回退到系統預設字體
    return pygame.font.SysFont(None, size)
