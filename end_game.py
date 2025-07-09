import pygame
from random import randint

SKILLS = ('shield', 'laser', 'knife')

class End_Game:
    def __init__(self, window):     
        self.window = window
        self.imgBG = pygame.image.load('static/photo/game_background.png')
        self.imgBG = pygame.transform.smoothscale(self.imgBG, (self.window.get_width(), self.window.get_height()))

        self.Eva_01 = Unit((350, self.window.get_height() * 0.5), pygame.image.load('static/photo/eva_01_ready.png'), 'knife')
        self.Eva_02 = Unit((200, 200), pygame.image.load('static/photo/eva_02_ready.png'), 'laser')
        self.Eva_00 = Unit((200, self.window.get_height() - 200), pygame.image.load('static/photo/eva_00_ready.png'), 'shield')

        self.Angel = Enemy((self.window.get_width() - 400, self.window.get_height() * 0.5), pygame.image.load('static/photo/angel_endgame.png'))
        self.alpha_surface = pygame.Surface((self.window.get_width(), self.window.get_height()), pygame.SRCALPHA)
        self.alpha_surface.fill((0, 0, 0, 180))

        self.font1 = pygame.font.Font('static/fonts/main_font.otf', 54)
        self.font2 = pygame.font.Font('static/fonts/main_font.otf', 55)
        self.menu_font = pygame.font.Font('static/fonts/main_font.otf', 20)

        self.timer = 60
        self.active = False
        

    def initialize(self):
        bg_rect = self.imgBG.get_rect(topleft = (0, 0))
        self.window.blit(self.imgBG, bg_rect)
        self.window.blit(self.alpha_surface, (0, 0))

        self.timer = (self.timer + 1) % 60
        if self.timer % 30 < 15: start_text = self.font2.render('Press any key to start...', True, 'white')
        else: start_text = self.font1.render('Press any key to start...', True, 'white')
        start_text_rect = start_text.get_rect(center = (self.window.get_width() // 2, self.window.get_height() - 100))
        self.window.blit(start_text, start_text_rect)

        start_text = self.font2.render('Speed typing', True, 'white')
        start_text_rect = start_text.get_rect(center = (self.window.get_width() // 2, 100))
        self.window.blit(start_text, start_text_rect)

        start_text = self.menu_font.render('Menu', True, 'white')
        start_text_rect = start_text.get_rect(bottomright=(140, self.window.get_height() - 30))
        self.window.blit(start_text, start_text_rect)
        mouse_pos = pygame.mouse.get_pos()
        if start_text_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.window, pygame.Color('white'), start_text_rect.inflate(10, 10), 3, 5)
            return 'menu'
        return None




    def play(self):
        bg_rect = self.imgBG.get_rect(topleft = (0, 0))
        self.window.blit(self.imgBG, bg_rect)

        # Eva_00_rect = self.Eva_00.img.get_rect(center = (self.Eva_00.position))
        # self.window.blit(self.Eva_00.img, Eva_00_rect)

        # Eva_01_rect = self.Eva_01.img.get_rect(center = (self.Eva_01.position))
        # self.window.blit(self.Eva_01.img, Eva_01_rect)

        # Eva_02_rect = self.Eva_02.img.get_rect(center = (self.Eva_02.position))
        # self.window.blit(self.Eva_02.img, Eva_02_rect)

        # Angel_rect = self.Angel.img.get_rect(center = (self.Angel.position))
        # self.window.blit(self.Angel.img, Angel_rect)

        pygame.draw.rect(self.window, 'green', self.Eva_00.rect)
        pygame.draw.rect(self.window, 'green', self.Eva_01.rect)
        pygame.draw.rect(self.window, 'green', self.Eva_02.rect)
        pygame.draw.rect(self.window, 'red', self.Angel.rect)

        start_text = self.menu_font.render('Menu', True, 'white')
        start_text_rect = start_text.get_rect(bottomright=(140, self.window.get_height() - 30))
        self.window.blit(start_text, start_text_rect)
        mouse_pos = pygame.mouse.get_pos()
        if start_text_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.window, pygame.Color('white'), start_text_rect.inflate(10, 10), 3, 5)
            return 'menu'


    def game_end(self):
        return False
    


    def contains(point, rect):
        return rect.collidepoint(point)
    
    def reset(self):
        self.active = False
        print('reset')


class Enemy:
    def __init__(self, position, img):
        self.position = position
        self.img = pygame.transform.smoothscale(img, (200, 300))
        self.rect = self.img.get_rect(center = (self.position))
        self.hp = 100
        self.attack_types = ['shield', 'attack']
        self.current_attack = None
        self.attack_power = 20

class Unit:
    def __init__(self, position, img, skill):
        self.position = position
        self.img = pygame.transform.smoothscale(img, (100, 100))
        self.rect = self.img.get_rect(center = (self.position))
        self.hp = 40
        self.skill = None

        