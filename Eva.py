from pygame.locals import *
import pygame

class EvaBullet:
    def __init__(self, x, y, speed, img=None, screen_width=800):
        self.px = x
        self.py = y
        self.speed = speed
        self.img = img
        self.width = img.get_width() if img else 8
        self.height = img.get_height() if img else 8
        self.screen_width = screen_width
        self.active = True

    def update(self):
        self.px += self.speed
        if self.px > self.screen_width:
            self.active = False

    def draw(self, window):
        if self.img:
            window.blit(self.img, (self.px, self.py - self.height//2))

    def get_rect(self):
        return pygame.Rect(self.px, self.py - self.height//2, self.width, self.height)

class Eva:
    def __init__(self, window, evaPX, evaPY, width, height, img, width_s, height_s, eva_bullets, bullet_img=None):
        self.window = window
        self.px = evaPX
        self.py = evaPY
        self.width = width
        self.height = height
        self.img = img
        self.width_s = width_s
        self.height_s = height_s
        self.eva_bullets = eva_bullets
        self.bullet_img = bullet_img
        self.last_shot_time = 0
        self.bullet_speed = 10

    def draw_eva(self):
        self.window.blit(self.img, (self.px, self.py))

    def eva_move(self, keys):
        if keys[K_UP] and self.py >= 30:
            self.py -= 10
        if keys[K_DOWN] and self.py <= self.height_s - self.height:
            self.py += 10
        if keys[K_RIGHT] and self.px <= self.width_s / 2:
            self.px += 10
        if keys[K_LEFT] and self.px >= 30:
            self.px -= 10

    def shooting(self, current_time_eva):
        if current_time_eva - self.last_shot_time > 500:
            self.eva_bullets.append(EvaBullet(
                self.px + self.width,
                self.py + self.height//2,
                self.bullet_speed,
                self.bullet_img,
                self.width_s
            ))
            self.last_shot_time = current_time_eva