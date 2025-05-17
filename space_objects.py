from OpenGL.GL import *
from OpenGL.GLU import *
import random
import numpy as np
from ..utils.config import *

class SpaceObject:
    def __init__(self, object_type="waste"):
        self.position = [
            random.uniform(MOVEMENT_BOUNDS['x'][0], MOVEMENT_BOUNDS['x'][1]),
            random.uniform(MOVEMENT_BOUNDS['y'][0], MOVEMENT_BOUNDS['y'][1]),
            MOVEMENT_BOUNDS['z'][0]
        ]
        self.speed = OBJECT_SPEED
        self.type = object_type
        self.active = True
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)

    def update(self):
        self.position[2] += self.speed
        self.rotation += self.rotation_speed
        if self.position[2] > MOVEMENT_BOUNDS['z'][1]:
            self.active = False

    def draw(self):
        if not self.active:
            return
            
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.rotation, 0, 1, 0)  # دوران حول محور Y
        
        if self.type == "waste":
            self._draw_waste()
        else:
            self._draw_crystal()
            
        glPopMatrix()

    def _draw_waste(self):
        # رسم النفايات كمكعب غير منتظم
        glBegin(GL_QUADS)
        glColor3f(0.7, 0.2, 0.2)  # أحمر
        
        # الوجه الأمامي
        glVertex3f(-0.15, -0.15, 0.15)
        glVertex3f(0.15, -0.15, 0.15)
        glVertex3f(0.15, 0.15, 0.15)
        glVertex3f(-0.15, 0.15, 0.15)
        
        # الوجه الخلفي
        glVertex3f(-0.15, -0.15, -0.15)
        glVertex3f(-0.15, 0.15, -0.15)
        glVertex3f(0.15, 0.15, -0.15)
        glVertex3f(0.15, -0.15, -0.15)
        
        # الوجه العلوي
        glVertex3f(-0.15, 0.15, -0.15)
        glVertex3f(-0.15, 0.15, 0.15)
        glVertex3f(0.15, 0.15, 0.15)
        glVertex3f(0.15, 0.15, -0.15)
        
        glEnd()

    def _draw_crystal(self):
        # رسم البلورة كهرم
        glBegin(GL_TRIANGLES)
        glColor3f(0.2, 0.7, 0.2)  # أخضر
        
        # القاعدة
        glVertex3f(-0.1, -0.1, 0.1)
        glVertex3f(0.1, -0.1, 0.1)
        glVertex3f(0.0, 0.2, 0.0)
        
        glVertex3f(0.1, -0.1, 0.1)
        glVertex3f(0.1, -0.1, -0.1)
        glVertex3f(0.0, 0.2, 0.0)
        
        glVertex3f(0.1, -0.1, -0.1)
        glVertex3f(-0.1, -0.1, -0.1)
        glVertex3f(0.0, 0.2, 0.0)
        
        glVertex3f(-0.1, -0.1, -0.1)
        glVertex3f(-0.1, -0.1, 0.1)
        glVertex3f(0.0, 0.2, 0.0)
        glEnd()

        # إضافة تأثير توهج
        glColor3f(0.3, 1.0, 0.3)  # أخضر فاتح
        glBegin(GL_LINES)
        for _ in range(8):
            angle = random.uniform(0, 2 * np.pi)
            length = random.uniform(0.15, 0.25)
            glVertex3f(0, 0, 0)
            glVertex3f(np.cos(angle) * length, np.sin(angle) * length, 0)
        glEnd() 