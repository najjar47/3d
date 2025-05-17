from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from ..utils.config import *

class SpaceShip:
    def __init__(self):
        self.position = [0, 0, 0]
        self.speed = PLAYER_SPEED
        self.energy = INITIAL_ENERGY
        self.score = 0
        self.rotation = 0  # زاوية دوران السفينة

    def move(self, direction):
        # تحديث الموقع
        self.position[0] += direction[0] * self.speed
        self.position[1] += direction[1] * self.speed
        
        # تحديث زاوية الدوران
        if direction[0] != 0:
            self.rotation = 20 if direction[0] > 0 else -20
        else:
            self.rotation = 0

        # تقييد الحركة ضمن الحدود
        self.position[0] = max(min(self.position[0], MOVEMENT_BOUNDS['x'][1]), MOVEMENT_BOUNDS['x'][0])
        self.position[1] = max(min(self.position[1], MOVEMENT_BOUNDS['y'][1]), MOVEMENT_BOUNDS['y'][0])

    def take_damage(self, damage):
        self.energy = max(0, self.energy - damage)
        return self.energy <= 0

    def add_energy(self, amount):
        self.energy = min(MAX_ENERGY, self.energy + amount)

    def add_score(self, points):
        self.score += points

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.rotation, 0, 0, 1)  # دوران حول محور Z
        
        # رسم جسم السفينة
        glBegin(GL_TRIANGLES)
        glColor3f(0.5, 0.5, 1.0)  # أزرق فاتح
        
        # المثلث الرئيسي
        glVertex3f(-0.2, -0.2, 0)
        glVertex3f(0.2, -0.2, 0)
        glVertex3f(0.0, 0.2, 0)
        
        # الأجنحة
        glColor3f(0.3, 0.3, 0.8)  # أزرق داكن
        glVertex3f(-0.3, -0.1, 0)
        glVertex3f(-0.2, -0.2, 0)
        glVertex3f(-0.1, -0.1, 0)
        
        glVertex3f(0.3, -0.1, 0)
        glVertex3f(0.2, -0.2, 0)
        glVertex3f(0.1, -0.1, 0)
        glEnd()
        
        # رسم محرك السفينة
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.5, 0.0)  # برتقالي
        glVertex3f(-0.1, -0.2, 0)
        glVertex3f(0.1, -0.2, 0)
        glVertex3f(0.1, -0.3, 0)
        glVertex3f(-0.1, -0.3, 0)
        glEnd()
        
        glPopMatrix() 