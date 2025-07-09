import pygame
from random import randint
import time


SKILLS = ('shield', 'laser', 'knife')

class End_Game:
    def __init__(self, window):     
        self.window = window
        self.imgBG = pygame.image.load('static/photo/game_background.png')
        self.imgBG = pygame.transform.smoothscale(self.imgBG, (self.window.get_width(), self.window.get_height()))

        self.Eva_01 = Unit((450, self.window.get_height() * 0.5), pygame.image.load('static/photo/eva_01_ready.png'), 'knife')
        self.Eva_02 = Unit((200, 300), pygame.image.load('static/photo/eva_02_ready.png'), 'laser')
        self.Eva_00 = Unit((200, self.window.get_height() - 300), pygame.image.load('static/photo/eva_00_ready.png'), 'shield')
        self.units = (self.Eva_01, self.Eva_00, self.Eva_02)

        self.Angel = Enemy((self.window.get_width() - 400, self.window.get_height() * 0.5), pygame.image.load('static/photo/angel_endgame.png'))
        self.alpha_surface = pygame.Surface((self.window.get_width(), self.window.get_height()), pygame.SRCALPHA)
        self.alpha_surface.fill((0, 0, 0, 180))

        self.font1 = pygame.font.Font('static/fonts/main_font.otf', 54)
        self.font2 = pygame.font.Font('static/fonts/main_font.otf', 55)
        self.menu_font = pygame.font.Font('static/fonts/main_font.otf', 20)

        self.timer = 60
        self.active = False

        self.selected_unit = None
        self.select = False

        self.players_steps = 2
        self.Angels_steps = 0

        self.need_to_down_steps = False

        self.imgField = pygame.image.load('static/photo/at.png')
        self.imgField = pygame.transform.smoothscale(self.imgField, (400, 500))
        self.imgField_Angel = pygame.image.load('static/photo/at_angel.png')
        self.imgField_Angel = pygame.transform.smoothscale(self.imgField_Angel, (600, 800))
        self.player_need_shield = False
        self.imgLaser = pygame.image.load('static/photo/laser(2).png')
        # self.imgLaser = pygame.transform.smoothscale(self.imgLaser, (100, 200))
        self.imgLaser = pygame.transform.rotate(self.imgLaser, -20)
        
        

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

        steps_count_text = self.font1.render('Steps left: ' + str(self.players_steps), True, 'white')
        steps_rect = steps_count_text.get_rect(center = (self.window.get_width() // 2, self.window.get_height() - 30))
        self.window.blit(steps_count_text, steps_rect)

        # pygame.draw.rect(self.window, 'green', self.Eva_00.rect)
        # pygame.draw.rect(self.window, 'green', self.Eva_01.rect)
        # pygame.draw.rect(self.window, 'green', self.Eva_02.rect)
        # pygame.draw.rect(self.window, 'red', self.Angel.rect)

        Eva_00_rect = self.Eva_00.img.get_rect(center = (self.Eva_00.position))
        self.window.blit(self.Eva_00.img, Eva_00_rect)
        pygame.draw.rect(self.window, 'red', (self.Eva_00.position[0] - 60, self.Eva_00.position[1] - 250, 160, 25))
        pygame.draw.rect(self.window, 'green', (self.Eva_00.position[0] - 60, self.Eva_00.position[1] - 250, self.Eva_00.hp * 4, 25))
        pygame.draw.rect(self.window, 'black', (self.Eva_00.position[0] - 64, self.Eva_00.position[1] - 254, 168, 33), 4, 8)

        Eva_01_rect = self.Eva_01.img.get_rect(center = (self.Eva_01.position))
        self.window.blit(self.Eva_01.img, Eva_01_rect)
        pygame.draw.rect(self.window, 'red', (self.Eva_01.position[0] - 60, self.Eva_01.position[1] - 250, 160, 25))
        pygame.draw.rect(self.window, 'green', (self.Eva_01.position[0] - 60, self.Eva_01.position[1] - 250, self.Eva_01.hp * 4, 25))
        pygame.draw.rect(self.window, 'black', (self.Eva_01.position[0] - 64, self.Eva_01.position[1] - 254, 168, 33), 4, 8)

        Eva_02_rect = self.Eva_02.img.get_rect(center = (self.Eva_02.position))
        self.window.blit(self.Eva_02.img, Eva_02_rect)
        pygame.draw.rect(self.window, 'red', (self.Eva_02.position[0] - 60, self.Eva_02.position[1] - 250, 160, 25))
        pygame.draw.rect(self.window, 'green', (self.Eva_02.position[0] - 60, self.Eva_02.position[1] - 250, self.Eva_02.hp * 4, 25))
        pygame.draw.rect(self.window, 'black', (self.Eva_02.position[0] - 64, self.Eva_02.position[1] - 254, 168, 33), 4, 8)

        Angel_rect = self.Angel.img.get_rect(center = (self.Angel.position))
        self.window.blit(self.Angel.img, Angel_rect)

        start_text = self.menu_font.render('Menu', True, 'white')
        start_text_rect = start_text.get_rect(bottomright=(140, self.window.get_height() - 30))
        self.window.blit(start_text, start_text_rect)

        to_return = None
        mouse_pos = pygame.mouse.get_pos()
        
        if start_text_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.window, pygame.Color('white'), start_text_rect.inflate(10, 10), 3, 5)
            to_return = 'menu'

        if self.players_steps > 0:
            if self.select and self.selected_unit is not None:
                self.use_skill(self.selected_unit)
                self.select = False
                self.selected_unit = None
                self.players_steps -= 1
                if self.players_steps == 0:
                    self.Angels_steps = 1

        elif self.Angels_steps == 1:
            time.sleep(0.5)
            self.Angel.use_skill()
            self.Angels_steps -= 1
            self.players_steps += 2
            time.sleep(0.5)
            self.player_need_shield = False

        if self.player_need_shield:
            rect = self.imgField.get_rect(center = (self.Eva_00.position[0] + 100, self.Eva_00.position[1] + 30))
            self.window.blit(self.imgField, rect)
            rect = self.imgField.get_rect(center = (self.Eva_01.position[0] + 100, self.Eva_01.position[1] + 30))
            self.window.blit(self.imgField, rect)
            rect = self.imgField.get_rect(center = (self.Eva_02.position[0] + 100, self.Eva_02.position[1] + 30))
            self.window.blit(self.imgField, rect)

        if self.Angel.need_shield:
            rect = self.imgField_Angel.get_rect(center = (self.Angel.position[0] - 170, self.Angel.position[1] + 50))
            self.window.blit(self.imgField_Angel, rect)

        return to_return
            

    def game_end(self):
        return False
    
    def check_for_select(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.players_steps > 0:
            for unit in self.units:
                if unit.rect.collidepoint(mouse_pos): 
                    # self.use_skill(unit)
                    # to_return = 'select'
                    self.select = True
                    self.selected_unit = unit
                    break
                else:
                    self.select = False

    
    def use_skill(self, unit):
        match unit.skill:
            case 'shield':
                self.player_need_shield = True
            case 'knife':
                pass
            case 'laser':
                self.window.blit(self.imgLaser, (700, 700))

    def contains(point, rect):
        return rect.collidepoint(point)
    
    def reset(self):
        self.active = False
        self.players_steps = 2
        self.Angels_steps = 0
        print('reset')


class Enemy:
    def __init__(self, position, img):
        self.position = position
        self.img = pygame.transform.smoothscale(img, (500, 700))
        self.rect = self.img.get_rect(center = (self.position))
        self.hp = 100
        self.attack_types = ['shield', 'attack']
        self.current_attack = None
        self.attack_power = 20
        self.need_shield = False

    def use_skill(self):
        self.current_attack = self.attack_types[randint(0,1)]
        print(self.current_attack)

        match self.current_attack:
            case 'shield':
                self.need_shield = True
            case 'attack':
                pass 

class Unit:
    def __init__(self, position, img, skill):
        self.position = position
        self.img = pygame.transform.smoothscale(img, (200, 400))
        self.rect = self.img.get_rect(center = (self.position))
        self.hp = 40
        self.skill = skill

        