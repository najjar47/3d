import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import arabic_reshaper
from bidi.algorithm import get_display
from .spaceship import SpaceShip
from .space_objects import SpaceObject
from ..utils.config import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        # إعداد النافذة
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("مغامرة الفضاء البيئية")
        
        # إعداد الكاميرا
        gluPerspective(45, (SCREEN_WIDTH/SCREEN_HEIGHT), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)
        
        # إعداد الخط
        self.font = pygame.font.Font(None, 36)
        
        # إعداد عناصر اللعبة
        self.ship = SpaceShip()
        self.space_objects = []
        self.game_over = False
        self.clock = pygame.time.Clock()

    def _reshape_arabic_text(self, text):
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)

    def spawn_object(self):
        if random.random() < SPAWN_RATE:
            object_type = "crystal" if random.random() < CRYSTAL_CHANCE else "waste"
            self.space_objects.append(SpaceObject(object_type))

    def check_collisions(self):
        ship_pos = np.array(self.ship.position)
        for obj in self.space_objects[:]:
            if not obj.active:
                continue
                
            obj_pos = np.array(obj.position)
            distance = np.linalg.norm(ship_pos - obj_pos)
            
            if distance < 0.4:
                if obj.type == "waste":
                    if self.ship.take_damage(WASTE_DAMAGE):
                        self.game_over = True
                else:  # crystal
                    self.ship.add_score(CRYSTAL_SCORE)
                    self.ship.add_energy(CRYSTAL_ENERGY)
                obj.active = False

    def draw_hud(self):
        # تحويل النص إلى صورة
        score_text = self._reshape_arabic_text(f"النقاط: {self.ship.score}")
        energy_text = self._reshape_arabic_text(f"الطاقة: {self.ship.energy}")
        
        score_surface = self.font.render(score_text, True, WHITE)
        energy_surface = self.font.render(energy_text, True, WHITE)
        
        # تحويل الصور إلى نسيج OpenGL
        def surface_to_texture(surface):
            data = pygame.image.tostring(surface, 'RGBA', True)
            texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surface.get_width(), surface.get_height(), 
                        0, GL_RGBA, GL_UNSIGNED_BYTE, data)
            return texture, surface.get_width(), surface.get_height()

        # رسم النصوص
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # رسم النقاط
        score_tex, w, h = surface_to_texture(score_surface)
        glBindTexture(GL_TEXTURE_2D, score_tex)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(10, 10)
        glTexCoord2f(1, 0); glVertex2f(10 + w, 10)
        glTexCoord2f(1, 1); glVertex2f(10 + w, 10 + h)
        glTexCoord2f(0, 1); glVertex2f(10, 10 + h)
        glEnd()

        # رسم الطاقة
        energy_tex, w, h = surface_to_texture(energy_surface)
        glBindTexture(GL_TEXTURE_2D, energy_tex)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(10, 50)
        glTexCoord2f(1, 0); glVertex2f(10 + w, 50)
        glTexCoord2f(1, 1); glVertex2f(10 + w, 50 + h)
        glTexCoord2f(0, 1); glVertex2f(10, 50 + h)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

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
        return True

    def update(self):
        self.spawn_object()
        
        # تحديث الكائنات
        for obj in self.space_objects[:]:
            obj.update()
            if not obj.active:
                self.space_objects.remove(obj)

        self.check_collisions()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # رسم الخلفية (نجوم)
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(0, 0, -10)
        glPointSize(2)
        glBegin(GL_POINTS)
        glColor3f(1, 1, 1)
        for _ in range(100):
            x = random.uniform(-10, 10)
            y = random.uniform(-10, 10)
            z = random.uniform(-5, 0)
            glVertex3f(x, y, z)
        glEnd()
        glPopMatrix()

        # رسم عناصر اللعبة
        self.ship.draw()
        for obj in self.space_objects:
            obj.draw()
            
        self.draw_hud()
        pygame.display.flip()

    def show_game_over(self):
        screen = pygame.display.get_surface()
        screen.fill(BLACK)
        
        game_over_text = self._reshape_arabic_text(f"انتهت اللعبة! النقاط: {self.ship.score}")
        game_over_surface = self.font.render(game_over_text, True, WHITE)
        
        screen_rect = screen.get_rect()
        text_rect = game_over_surface.get_rect(center=screen_rect.center)
        
        screen.blit(game_over_surface, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)

    def run(self):
        running = True
        while running and not self.game_over:
            self.clock.tick(FPS)
            running = self.handle_input()
            self.update()
            self.draw()

        if self.game_over:
            self.show_game_over() 