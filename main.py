"""
نقطة البداية للعبة مغامرة الفضاء البيئية
"""

import sys
import pygame
from src.game.game import Game

def main():
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"حدث خطأ: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main() 