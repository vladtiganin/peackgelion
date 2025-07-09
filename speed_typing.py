import pygame
from random import randint

class Speed_Typing:
    def __init__(self, window):
        self.window = window
        self.active = False
        self.timer = 60
        self.dasplay_timer = 5 # чтобы долго не ждать 
        self.words = ["shinji","rei","asuka","kaworu","gendo",
                      "misato","ritsuko","seele","lilith","adam",
                      "evangelion","lcl","angel","nerv",
                      "spear","instrumentality","hedgehog","dummy","impact"]
        self.font1 = pygame.font.Font('static/fonts/main_font.otf', 54)
        self.font2 = pygame.font.Font('static/fonts/main_font.otf', 55)
        self.need_to_generate = True
        self.current_word = None
        self.score = 0

        self.menu_font = pygame.font.Font('static/fonts/main_font.otf', 20)
        self.menu_text = self.menu_font.render('Menu', True, 'White')
        self.menu_rect = self.menu_text.get_rect(bottomright=(140, self.window.get_height() - 30))
        self.game_end = False



    def initialize(self):
        self.window.fill((30, 30, 30))

        self.timer = (self.timer + 1) % 60
        if self.timer % 30 < 15: start_text = self.font2.render('Press any key to start...', True, 'white')
        else: start_text = self.font1.render('Press any key to start...', True, 'white')
        start_text_rect = start_text.get_rect(center = (self.window.get_width() // 2, self.window.get_height() - 100))
        self.window.blit(start_text, start_text_rect)

        start_text = self.font2.render('Speed typing', True, 'white')
        start_text_rect = start_text.get_rect(center = (self.window.get_width() // 2, 100))
        self.window.blit(start_text, start_text_rect)

        for i in range(7):
            xPos = int(self.window.get_width() / 2 - 90 * 3.5 + i * 90) # 70 = 50 + 20; 2.5 = 5/2; вместо 5 далее будет len(word)
            yPos = self.window.get_height() // 3 + 70

            rect = pygame.Rect((xPos - 4, yPos - 4), (78, 88))           
            pygame.draw.rect(self.window, 'black', rect, 4, 5)

            rect = pygame.Rect((xPos, yPos), (70, 80))
            pygame.draw.rect(self.window, (208, 208, 208),rect)

        self.window.blit(self.menu_text, self.menu_rect)
        mouse_pos = pygame.mouse.get_pos()
        if self.menu_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.window, pygame.Color('black'), self.menu_rect.inflate(10, 10), 3, 5)
            return 'menu'
        return None



    def play(self, input_word):
        if self.dasplay_timer == 0: self.game_end = True

        start_text = self.font2.render('Speed typing', True, 'white')
        start_text_rect = start_text.get_rect(center = (self.window.get_width() // 2, 100))
        self.window.blit(start_text, start_text_rect)

        start_text = self.font2.render('Score: ' + str(self.score), True, 'white')
        start_text_rect = start_text.get_rect(topleft = (30, 20))
        self.window.blit(start_text, start_text_rect)

        start_text = self.font2.render('Time left: ' + str(self.dasplay_timer), True, 'white')
        start_text_rect = start_text.get_rect(topright = (self.window.get_width() - 30, 20))
        self.window.blit(start_text, start_text_rect)
        self.timer = (self.timer + 1) % 60
        if self.timer % 60 == 0: self.dasplay_timer -= 1

        if self.need_to_generate:
            self.current_word = self.words[randint(0, len(self.words) - 1)]
            self.need_to_generate = False
            print(self.current_word)
            

        for i, char in enumerate(self.current_word):
            xPos = int(self.window.get_width() / 2 - 90 * float(len(self.current_word)) / 2 + i * 90) # 70 = 50 + 20; 2.5 = 5/2; вместо 5 далее будет len(word)
            yPos = self.window.get_height() // 3 + 70

            rect = pygame.Rect((xPos - 4, yPos - 4), (78, 88))           
            pygame.draw.rect(self.window, (173, 173, 173), rect, 4, 5)

            if i < len(input_word):
                if char == input_word[i] : 
                    pygame.draw.rect(self.window, (34, 255, 42), rect, 4, 5)
                else:
                    pygame.draw.rect(self.window, (241, 0, 0), rect, 4, 5)

            rect = pygame.Rect((xPos, yPos), (70, 80))
            pygame.draw.rect(self.window, (208, 208, 208),rect)

            char = self.font2.render(char, True, 'black')
            char_rect = char.get_rect(center = (xPos + rect.width // 2, yPos + rect.height // 2 - 5))
            self.window.blit(char, char_rect)

            if input_word == self.current_word:
                self.need_to_generate = True
                self.score += 5
                return True
        
        self.window.blit(self.menu_text, self.menu_rect)
        mouse_pos = pygame.mouse.get_pos()
        if self.menu_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.window, pygame.Color('white'), self.menu_rect.inflate(10, 10), 3, 5)
            return 'menu'
        
        return False
    

    def end_window(self):
        if self.score <= -20:
            to_return = None

            font_main = pygame.font.Font('static/fonts/main_font.otf', 70)
            start_text = font_main.render('Game over...', True, 'white')
            start_text_rect = start_text.get_rect(center = (self.window.get_width() // 2, self.window.get_height() // 3))
            self.window.blit(start_text, start_text_rect)

            start_text = self.font2.render('You need to score 25 points', True, 'white')
            start_text_rect = start_text.get_rect(center = (self.window.get_width() // 2, self.window.get_height() // 3 + 170))
            self.window.blit(start_text, start_text_rect)

            start_text = self.font2.render('Your score: ' + str(self.score), True, 'white')
            start_text_rect = start_text.get_rect(center = (self.window.get_width() // 2, self.window.get_height() // 3 + 270))
            self.window.blit(start_text, start_text_rect)

            text = self.font1.render('Try again', True, 'white')
            text_rect = text.get_rect(center = (self.window.get_width() // 2, self.window.get_height() // 3 + 470))
            self.window.blit(text, text_rect)
            mouse_pos = pygame.mouse.get_pos()
            if text_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.window, pygame.Color('white'), text_rect.inflate(10, 10), 3, 5)
                to_return = 'again'
            
            self.window.blit(self.menu_text, self.menu_rect)
            mouse_pos = pygame.mouse.get_pos()
            if self.menu_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.window, pygame.Color('white'), self.menu_rect.inflate(10, 10), 3, 5)
                to_return = 'menu'

            if to_return != None: return to_return
        
        else:
            to_return = None

            font_main = pygame.font.Font('static/fonts/main_font.otf', 70)
            start_text = font_main.render('You win!', True, 'white')
            start_text_rect = start_text.get_rect(center = (self.window.get_width() // 2, self.window.get_height() // 3 ))
            self.window.blit(start_text, start_text_rect)

            start_text = self.font2.render('Your score: ' + str(self.score), True, 'white')
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

            self.window.blit(self.menu_text, self.menu_rect)
            mouse_pos = pygame.mouse.get_pos()
            if self.menu_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.window, pygame.Color('white'), self.menu_rect.inflate(10, 10), 3, 5)
                to_return = 'menu'
            
            if to_return != None: return to_return
            


    def reset(self):
        self.need_to_generate = True
        self.current_word = None
        self.score = 0
        self.game_end = False
        self.dasplay_timer = 30
        self.active = False
