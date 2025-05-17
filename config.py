"""
إعدادات اللعبة
"""

# إعدادات الشاشة
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# إعدادات اللعبة
PLAYER_SPEED = 0.1
OBJECT_SPEED = 0.1
SPAWN_RATE = 0.02
CRYSTAL_CHANCE = 0.3

# الألوان
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# حدود الحركة
MOVEMENT_BOUNDS = {
    'x': (-5, 5),
    'y': (-3, 3),
    'z': (-15, 5)
}

# نقاط وطاقة
CRYSTAL_SCORE = 100
CRYSTAL_ENERGY = 20
WASTE_DAMAGE = 10
INITIAL_ENERGY = 100
MAX_ENERGY = 100 