import pygame
from random import randint
import time


SKILLS = ('shield', 'laser', 'knife')

class End_Game:
    def __init__(self, window):     
        self.window = window
        self.imgBG = pygame.image.load('static/photo/game_background.png')
        self.imgBG = pygame.transform.smoothscale(self.imgBG, (self.window.get_width(), self.window.get_height()))

        self.Eva_01 = Unit((450, self.window.get_height() * 0.5), pygame.image.load('static/photo/eva_01.png'), 'knife')
        self.Eva_02 = Unit((200, 350), pygame.image.load('static/photo/eva_02.png'), 'laser')
        self.Eva_00 = Unit((200, self.window.get_height() - 300), pygame.image.load('static/photo/eva_00.png'), 'shield')
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
        self.is_laser_attack = False
        self.is_knife_attack = False
        self.laser_timer = 0
        self.knife_timer = 0
        self.imgLaser = pygame.image.load('static/photo/new_laser.png')
        self.imgLaser = pygame.transform.smoothscale(self.imgLaser, (80, 160))
        self.imgLaser = pygame.transform.rotate(self.imgLaser, 76)
        self.imgKnife = pygame.image.load('static/photo/knife_in_hand.png')
        self.imgKnife = pygame.transform.smoothscale(self.imgKnife, (110, 70))

        self.is_angel_attack = False
        self.angel_timer = 0
        self.imgAngel_ball = pygame.image.load('static/photo/angel_ball.png')
        self.imgAngel_ball = pygame.transform.smoothscale(self.imgAngel_ball, (120, 100))

        self.is_animating_units = False
        self.is_animating_Angel = False

        self.is_end = False
        self.is_end_timer = 90
        self.is_click = True

        self.is_music_playing = False
        self.congratulations = pygame.mixer.Sound('static/music/congratulations.wav')
        self.lose_sound = pygame.mixer.Sound('static/music/lose.wav')

        self.is_Angel_waite = False
        #timer
        

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
        pygame.draw.rect(self.window, 'red', (self.Eva_00.position[0] - 60, self.Eva_00.position[1] - 280, 160, 25))
        pygame.draw.rect(self.window, 'green', (self.Eva_00.position[0] - 60, self.Eva_00.position[1] - 280, self.Eva_00.hp * 4, 25))
        pygame.draw.rect(self.window, 'black', (self.Eva_00.position[0] - 64, self.Eva_00.position[1] - 284, 168, 33), 4, 8)


        if self.is_knife_attack and self.is_animating_units:
            self.knife_attack()
            if self.knife_timer == 0:
                self.is_knife_attack = False
                self.is_animating = False
        else:
            Eva_01_rect = self.Eva_01.img.get_rect(center = (self.Eva_01.position))
            self.window.blit(self.Eva_01.img, Eva_01_rect)
            knife_rect = self.imgKnife.get_rect(center = (self.Eva_01.position[0] - 10, self.Eva_01.position[1] + 14))
            self.window.blit(self.imgKnife, knife_rect)
            pygame.draw.rect(self.window, 'red', (self.Eva_01.position[0] - 80, self.Eva_01.position[1] - 270, 160, 25))
            pygame.draw.rect(self.window, 'green', (self.Eva_01.position[0] - 80, self.Eva_01.position[1] - 270, self.Eva_01.hp * 4, 25))
            pygame.draw.rect(self.window, 'black', (self.Eva_01.position[0] - 84, self.Eva_01.position[1] - 274, 168, 33), 4, 8)


        Eva_02_rect = self.Eva_02.img.get_rect(center = (self.Eva_02.position))
        self.window.blit(self.Eva_02.img, Eva_02_rect)
        pygame.draw.rect(self.window, 'red', (self.Eva_02.position[0] - 80, self.Eva_02.position[1] - 280, 160, 25))
        pygame.draw.rect(self.window, 'green', (self.Eva_02.position[0] - 80, self.Eva_02.position[1] - 280, self.Eva_02.hp * 4, 25))
        pygame.draw.rect(self.window, 'black', (self.Eva_02.position[0] - 84, self.Eva_02.position[1] - 284, 168, 33), 4, 8)

        Angel_rect = self.Angel.img.get_rect(center = (self.Angel.position))
        self.window.blit(self.Angel.img, Angel_rect)
        pygame.draw.rect(self.window, 'red', (self.Angel.position[0] - 160, self.Angel.position[1] - 350, 200, 25))
        pygame.draw.rect(self.window, 'green', (self.Angel.position[0] - 160, self.Angel.position[1] - 350, self.Angel.hp * 4, 25))
        pygame.draw.rect(self.window, 'black', (self.Angel.position[0] - 164, self.Angel.position[1] - 354, 208, 33), 4, 8)

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
                    self.is_Angel_waite = True
                    self.angel_timer = 60
        elif self.Angels_steps == 1:
            if self.is_Angel_waite:
                self.angel_timer -= 1
                if self.angel_timer == 0:
                    self.is_Angel_waite = False
            else:
                # time.sleep(0.5)
                self.use_angels_skill()
                self.Angels_steps -= 1
                self.players_steps += 2
                #time.sleep(0.5)
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

        if self.is_animating_units:
            if self.is_laser_attack:
                self.laser_attack()
                if self.laser_timer == 0:
                    self.is_laser_attack = False
                    self.is_animating_units = False


        if self.is_animating_Angel:
            if self.is_angel_attack:
                print(f"Angel attack! Timer: {self.angel_timer}, Target: {self.unit_to_attack.position}")
                self.angel_attack()
                if self.angel_timer == 0:
                    self.is_angel_attack = False 
                    self.is_animating_Angel = False   

        if self.Eva_00.hp == 0 or self.Eva_01.hp == 0 or self.Eva_02.hp == 0 or self.Angel.hp == 0:
            self.is_click = False
            self.is_end_timer -= 1
            if self.is_end_timer == 0:
                self.is_end = True

        return to_return
            
    def game_end(self):
        if self.Eva_00.hp == 0 or self.Eva_01.hp == 0 or self.Eva_02.hp == 0:
            to_return = None

            if not self.is_music_playing:
                self.lose_sound.play()
                self.is_music_playing = True

            font_main = pygame.font.Font('static/fonts/main_font.otf', 70)
            start_text = font_main.render('Game over...', True, 'white')
            start_text_rect = start_text.get_rect(center = (self.window.get_width() // 2, self.window.get_height() // 3))
            self.window.blit(start_text, start_text_rect)

            start_text = self.font2.render('One of the Eva pilots died...', True, 'white')
            start_text_rect = start_text.get_rect(center = (self.window.get_width() // 2, self.window.get_height() // 3 + 170))
            self.window.blit(start_text, start_text_rect)

            text = self.font1.render('Try again', True, 'white')
            text_rect = text.get_rect(center = (self.window.get_width() // 2, self.window.get_height() // 3 + 470))
            self.window.blit(text, text_rect)
            mouse_pos = pygame.mouse.get_pos()
            if text_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.window, pygame.Color('white'), text_rect.inflate(10, 10), 3, 5)
                to_return = 'again'
            

            menu_font = pygame.font.Font('static/fonts/main_font.otf', 20)
            menu_text = menu_font.render('Menu', True, 'White')
            menu_rect = menu_text.get_rect(bottomright=(140, self.window.get_height() - 30))
            self.window.blit(menu_text, menu_rect)
            mouse_pos = pygame.mouse.get_pos()
            if menu_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.window, pygame.Color('white'), menu_rect.inflate(10, 10), 3, 5)
                to_return = 'menu'

            if to_return != None: return to_return
        
        else:
            to_return = None

            if not self.is_music_playing:
                self.congratulations.play()
                self.is_music_playing = True

            font_main = pygame.font.Font('static/fonts/main_font.otf', 70)
            start_text = font_main.render('You win!', True, 'white')
            start_text_rect = start_text.get_rect(center = (self.window.get_width() // 2, self.window.get_height() // 3 ))
            self.window.blit(start_text, start_text_rect)

            start_text = self.font2.render('The angel is defeated! ', True, 'white')
            start_text_rect = start_text.get_rect(center = (self.window.get_width() // 2, self.window.get_height() // 3 + 170))
            self.window.blit(start_text, start_text_rect)

            text = self.font1.render('Try again', True, 'white')
            text_rect = text.get_rect(center = (self.window.get_width() // 2 - 200, self.window.get_height() // 3 + 470))
            self.window.blit(text, text_rect)
            mouse_pos = pygame.mouse.get_pos()
            if text_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.window, pygame.Color('white'), text_rect.inflate(10, 10), 3, 5)
                to_return = 'again'
            
            text = self.font1.render('Continue', True, 'white')
            text_rect = text.get_rect(center = (self.window.get_width() // 2 + 200, self.window.get_height() // 3 + 470))
            self.window.blit(text, text_rect)
            mouse_pos = pygame.mouse.get_pos()
            if text_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.window, pygame.Color('white'), text_rect.inflate(10, 10), 3, 5)
                to_return = 'continue'

            menu_font = pygame.font.Font('static/fonts/main_font.otf', 20)
            menu_text = menu_font.render('Menu', True, 'White')
            menu_rect = menu_text.get_rect(bottomright=(140, self.window.get_height() - 30))
            self.window.blit(menu_text, menu_rect)
            mouse_pos = pygame.mouse.get_pos()
            if menu_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.window, pygame.Color('white'), menu_rect.inflate(10, 10), 3, 5)
                to_return = 'menu'
            
            if to_return != None: return to_return
    
    def check_for_select(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.players_steps > 0 and self.is_click:
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
                self.knife_timer = 40
                self.is_knife_attack = True
                #self.Angel.need_shield = False
                self.is_animating_units = True
            case 'laser':
                self.laser_timer = 15
                self.is_laser_attack = True
                self.is_animating_units = True
                if not self.Angel.need_shield:
                    self.Angel.hp -= 5
    
    def reset(self):
        self.active = False
        self.players_steps = 2
        self.Angels_steps = 0
        self.selected_unit = None
        self.select = False

        self.timer = 60
        self.active = False

        self.selected_unit = None
        self.select = False

        self.players_steps = 2
        self.Angels_steps = 0

        self.need_to_down_steps = False
        self.player_need_shield = False
        self.is_laser_attack = False
        self.is_knife_attack = False
        self.laser_timer = 0
        self.knife_timer = 0
        self.is_angel_attack = False
        self.angel_timer = 0
        self.is_animating_units = False
        self.is_animating_Angel = False

        self.Eva_00.hp = 40
        self.Eva_01.hp = 40
        self.Eva_02.hp = 40
        self.Angel.hp = 50
        self.Angel.current_attack = None
        self.Angel.need_shield = False
        
        self.is_end = False
        self.is_end_timer = 60

        self.is_music_playing = True
        self.is_click = True

        print('reset')

    def laser_attack(self):
        startX, startY = self.Eva_02.position
        stepX = (self.Angel.position[0] - self.Eva_02.position[0] - 150) / 15
        stepY = (self.Angel.position[1] - self.Eva_02.position[1]) / 15
        self.window.blit(self.imgLaser, (startX + stepX * (16 - self.laser_timer), startY + stepY * (16 - self.laser_timer)))
        self.laser_timer -= 1

    def knife_attack(self):
        current_pos = None
        if self.knife_timer > 20:
            startX, startY = self.Eva_01.position[0],  self.Eva_01.position[1] - 190
            stepX = (self.Angel.position[0] - self.Eva_01.position[0] - 250) / 20
            #stepY = (self.Angel.position[1] - self.Eva_01.position[1] + 200) / 30
            current_pos = ((startX + stepX * (41 - self.knife_timer), startY - 20))
            self.window.blit(self.Eva_01.img, current_pos)
            self.window.blit(self.imgKnife, current_pos)
            self.knife_timer -= 1
        else:
            self.Angel.need_shield = False
            startX, startY = self.Angel.position[0] - 100, self.Eva_01.position[1] - 190
            stepX = -(self.Angel.position[0] - self.Eva_01.position[0] - 150) / 20
            # stepY = -(self.Angel.position[1] - self.Eva_01.position[1] + 200) / 30
            current_pos = ((startX + stepX * (21 - self.knife_timer), startY - 20))
            self.window.blit(self.Eva_01.img, current_pos)
            self.window.blit(self.imgKnife, current_pos)
            self.knife_timer -= 1


    def angel_attack(self):
        startX, startY = self.Angel.position
        stepX = -(self.Angel.position[0] - self.unit_to_attack.position[0] - 150) / 15
        stepY = -(self.Angel.position[1] - self.unit_to_attack.position[1]) / 15
        self.window.blit(self.imgAngel_ball, (startX + stepX * (16 - self.angel_timer), startY + stepY * (16 - self.angel_timer)))
        self.angel_timer -= 1


    def use_angels_skill(self):
        self.Angel.current_attack = self.Angel.attack_types[int(float(randint(0,140)) / 100)]
        print(self.Angel.current_attack)

        match self.Angel.current_attack:
            case 'shield':
                self.Angel.need_shield = True
            case 'attack':
                self.is_angel_attack = True
                self.angel_timer = 15
                self.unit_to_attack = self.units[randint(0, 2)]
                if not self.player_need_shield : self.unit_to_attack.hp -= 20
                self.is_animating_Angel = True

    
class Enemy:
    def __init__(self, position, img):
        self.position = position
        self.img = pygame.transform.smoothscale(img, (500, 700))
        self.rect = self.img.get_rect(center = (self.position))
        self.hp = 50 
        self.attack_types = ['attack', 'shield']
        self.current_attack = None
        self.attack_power = 20
        self.need_shield = False


class Unit:
    def __init__(self, position, img, skill):
        self.position = position
        self.img = pygame.transform.smoothscale(img, (200, 500))
        self.rect = self.img.get_rect(center = (self.position))
        self.hp = 40
        self.skill = skill

        