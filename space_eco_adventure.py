import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random

# تهيئة Pygame و OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("مغامرة الفضاء البيئية")

# إعدادات الكاميرا
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

class SpaceShip:
    def __init__(self):
        self.position = [0, 0, 0]
        self.speed = 0.1
        self.collected_items = 0
        self.energy = 100

    def move(self, direction):
        self.position[0] += direction[0] * self.speed
        self.position[1] += direction[1] * self.speed
        # تقييد حركة السفينة ضمن حدود معينة
        self.position[0] = max(min(self.position[0], 5), -5)
        self.position[1] = max(min(self.position[1], 3), -3)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        
        # رسم السفينة (مؤقتاً كمثلث بسيط)
        glBegin(GL_TRIANGLES)
        glColor3f(0.5, 0.5, 1.0)
        glVertex3f(-0.2, -0.2, 0)
        glVertex3f(0.2, -0.2, 0)
        glVertex3f(0.0, 0.2, 0)
        glEnd()
        
        glPopMatrix()

class SpaceObject:
    def __init__(self, object_type="waste"):
        self.position = [random.uniform(-5, 5), random.uniform(-3, 3), -15]
        self.speed = 0.1
        self.type = object_type  # "waste" or "crystal"
        self.active = True

    def update(self):
        self.position[2] += self.speed
        if self.position[2] > 5:
            self.active = False

    def draw(self):
        if not self.active:
            return
            
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        
        # رسم الكائن (مؤقتاً ككرة بسيطة)
        if self.type == "waste":
            glColor3f(0.7, 0.2, 0.2)  # أحمر للنفايات
        else:
            glColor3f(0.2, 0.7, 0.2)  # أخضر للكريستال
            
        glutSolidSphere(0.2, 16, 16)
        glPopMatrix()

class Game:
    def __init__(self):
        self.ship = SpaceShip()
        self.space_objects = []
        self.score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 36)

    def spawn_object(self):
        if random.random() < 0.02:  # احتمالية ظهور كائن جديد
            object_type = "crystal" if random.random() < 0.3 else "waste"
            self.space_objects.append(SpaceObject(object_type))

    def check_collisions(self):
        ship_pos = np.array(self.ship.position)
        for obj in self.space_objects:
            if not obj.active:
                continue
                
            obj_pos = np.array(obj.position)
            distance = np.linalg.norm(ship_pos - obj_pos)
            
            if distance < 0.4:  # مسافة التصادم
                if obj.type == "waste":
                    self.ship.energy -= 10
                    if self.ship.energy <= 0:
                        self.game_over = True
                else:  # crystal
                    self.score += 100
                    self.ship.energy = min(100, self.ship.energy + 20)
                obj.active = False

    def draw_hud(self):
        # رسم معلومات اللعبة
        score_surface = self.font.render(f"النقاط: {self.score}", True, (255, 255, 255))
        energy_surface = self.font.render(f"الطاقة: {self.ship.energy}", True, (255, 255, 255))
        
        screen = pygame.display.get_surface()
        screen.blit(score_surface, (10, 10))
        screen.blit(energy_surface, (10, 40))

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            # التحكم بالسفينة
            keys = pygame.key.get_pressed()
            direction = [0, 0, 0]
            if keys[pygame.K_LEFT]:
                direction[0] = -1
            if keys[pygame.K_RIGHT]:
                direction[0] = 1
            if keys[pygame.K_UP]:
                direction[1] = 1
            if keys[pygame.K_DOWN]:
                direction[1] = -1
            self.ship.move(direction)

            # تحديث الكائنات
            self.spawn_object()
            for obj in self.space_objects[:]:
                obj.update()
                if not obj.active:
                    self.space_objects.remove(obj)

            self.check_collisions()

            # الرسم
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.ship.draw()
            for obj in self.space_objects:
                obj.draw()
            
            pygame.display.flip()
            pygame.time.wait(10)

        # عرض شاشة انتهاء اللعبة
        screen = pygame.display.get_surface()
        screen.fill((0, 0, 0))
        game_over_surface = self.font.render(f"انتهت اللعبة! النقاط: {self.score}", True, (255, 255, 255))
        screen.blit(game_over_surface, (display[0]//2 - 100, display[1]//2))
        pygame.display.flip()
        pygame.time.wait(2000)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit() 