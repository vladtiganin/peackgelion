import pygame
import os

class AngelBullet:
    def __init__(self, x, y, speed, img=None):
        self.px = x
        self.py = y
        self.speed = speed
        self.img = img
        self.width = img.get_width() if img else 8
        self.height = img.get_height() if img else 8
        self.active = True

    def update(self, screen_width):
        self.px -= self.speed
        if self.px + self.width < 0:  # Полностью за левой границей
            self.active = False

    def draw(self, window):
        if self.img:
            window.blit(self.img, (self.px, self.py - self.height//2))
    
    # Добавляем метод get_rect() для совместимости
    def get_rect(self):
        return pygame.Rect(self.px, self.py - self.height//2, self.width, self.height)

class Angel:
    def __init__(self, window, x, y, screen_width, screen_height, angel_bullets, bullet_img=None, angel_img=None):
        self.window = window
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.angel_bullets = angel_bullets
        self.bullet_img = bullet_img
        self.move_direction = 1
        self.speed = 3
        self.last_shot_time = 0
        self.shoot_delay = 1500
        self.DEBUG_MODE = False

        try:
            self.img = pygame.image.load('static/photo/Angel.png').convert_alpha()
            self.img = pygame.transform.scale(self.img, (150, 150))
        except:
            self.img = pygame.Surface((150, 150), pygame.SRCALPHA)
            pygame.draw.circle(self.img, (255, 0, 0, 255), (75, 75), 75)
        self.img_width = self.img.get_width()
        self.img_height = self.img.get_height()

    def update(self, current_time):
        # Движение с проверкой границ
        self.y = max(30, min(self.y + self.speed * self.move_direction, self.screen_height - 180))
        if self.y <= 30 or self.y >= self.screen_height - 180:
            self.move_direction *= -1
        
        # Стрельба с ограничением
        if current_time - self.last_shot_time > self.shoot_delay and len(self.angel_bullets) < 5:
            self.shoot()
            self.last_shot_time = current_time
        
        # Обновление пуль
        for bullet in self.angel_bullets[:]:
            bullet.update(self.screen_width)
            if not bullet.active:
                self.angel_bullets.remove(bullet)

    def shoot(self):
        self.angel_bullets.append(AngelBullet(
            self.x - self.img_width//2,
            self.y + self.img_height//2,
            12,
            self.bullet_img
        ))

    def draw(self):
        draw_x = min(self.x - self.img_width//2, self.screen_width - self.img_width)
        draw_y = min(max(self.y, 0), self.screen_height - self.img_height)
        self.window.blit(self.img, (draw_x, draw_y))