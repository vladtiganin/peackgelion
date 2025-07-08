import pygame
import re
import keyboard

class Dialog:
    def __init__(self, window, file_path, *girls):
        self.Misato, self.Rei, self.Asuka = girls
        self.file_path = file_path
        self.dir = self.mk_dir(self.file_path)
        self.width = window.get_width() - 100
        self.height = window.get_height() * 0.25
        self.x = (window.get_width() - self.width) // 2
        self.y = window.get_height() - self.height
        self.window = window
        self.active = True
        self.current_pos = 0

        self.dialog_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # self.background_color = (255, 195, 27, 200)  
        # self.border_color = (224, 120, 0, 255)       
        self.text_color = (0, 0, 0, 255)             

        self.text_font = pygame.font.Font('static/fonts/main_font.otf', 37)
        self.menu_font = pygame.font.Font('static/fonts/main_font.otf', 20)
        self.name_font = pygame.font.Font('static/fonts/main_font.otf', 50)
        self.menu_text = self.menu_font.render('Menu', True, 'black')
        self.menu_rect = self.menu_text.get_rect(bottomright=(140, self.window.get_height() - 30))


        self.imgBG = pygame.image.load('static/photo/bg_dialog_1.jpg')
        self.imgBG = pygame.transform.scale(self.imgBG, (self.window.get_width(), self.window.get_height()))
        # self.imgMisato = pygame.image.load('static/photo/misato_ready.png')
        # self.imgRei = pygame.image.load('static/photo/rei_dress-up.png')
        # self.imgAsuka = pygame.image.load('static/photo/asuka_dress-up.png')

    def mk_dir(self, path):
        dialogue = []
        
        with open(path, 'r') as file:
            content = file.read()
            lines = content.split('\n')
            for line in lines:
                    line = line.strip().replace('character: ', '')
                    if '; text: ' not in line:  
                        continue
                    
                    pair = line.split('; text: ')
                    if len(pair) != 2:  
                        continue
                    
                    character = pair[0].strip()
                    text = pair[1].strip().strip('"')
                    
                    dialogue.append({'character': character, 'text': text})  


        return dialogue
            
            
    def next(self):
        if self.current_pos < len(self.dir) -1: 
            self.current_pos += 1
            return True
        else: return False


    def define_girl(self):
        match self.dir[self.current_pos]['character']:
            case 'Misato': return self.Misato
            case 'Rei': return self.Rei
            case 'Asuka': return self.Asuka


    def draw(self):
        if not self.active: 
            return False

        self.window.blit(self.imgBG, (0, 0))
        # misato_rect = self.imgMisato.get_rect(center=(self.window.get_width() // 8 * 6, self.window.get_height() // 5 * 3))
        # self.window.blit(self.imgMisato, misato_rect)

        #self.dialog_surface.fill((0, 0, 0, 0))
        current_girl = self.define_girl()

        girl_rect = current_girl.img.get_rect(center=(current_girl.position))
        self.window.blit(current_girl.img, girl_rect)
        pygame.draw.rect(self.dialog_surface, current_girl.background_color, (4, 4, self.width - 8, self.height - 8))
        pygame.draw.rect(self.dialog_surface, current_girl.border_color, (0, 0, self.width, self.height), 4)
        
        self.window.blit(self.dialog_surface, (self.x, self.y))

        #character = self.dir[self.current_pos]['character'] 
        text = self.dir[self.current_pos]['text']

        current_name = self.name_font.render(current_girl.name + ':', True, 'black')
        name_rect = current_name.get_rect(topleft = (self.x + 30, self.y + 15))
        self.window.blit(current_name, name_rect)


        text_x = self.x + 30
        text_y = self.y + 75
        current_x = text_x
        current_y = text_y

        words = text.split(' ')
        for word in words:
            word_surface = self.text_font.render(word + ' ', True, self.text_color)
            if current_x + word_surface.get_width() > self.x + self.width - 30:
                current_y += word_surface.get_height() + 5
                current_x = text_x
            self.window.blit(word_surface, (current_x, current_y))
            current_x += word_surface.get_width()

        self.window.blit(self.menu_text, self.menu_rect)
    
        mouse_pos = pygame.mouse.get_pos()
        if self.menu_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.window, pygame.Color('black'), self.menu_rect.inflate(10, 10), 3, 5)
            return True
            
        