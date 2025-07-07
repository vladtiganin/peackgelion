import pygame

class Dialog:
    def __init__(self, window, text):
        self.text = text
        self.width = window.get_width() - 100
        self.height = window.get_height() * 0.25
        self.x = (window.get_width() - self.width) // 2
        self.y = window.get_height() - self.height
        self.window = window
        self.active = True

        # Создаем поверхность с прозрачностью для диалога
        self.dialog_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        

        self.background_color = (255, 195, 27, 200)  
        self.border_color = (224, 120, 0, 255)       
        self.text_color = (0, 0, 0, 255)             

        self.text_font = pygame.font.Font('static/fonts/main_font.otf', 37)
        self.menu_font = pygame.font.Font('static/fonts/main_font.otf', 20)
        self.menu_text = self.menu_font.render('Menu', True, 'black')
        self.menu_rect = self.menu_text.get_rect(bottomright=(120, self.window.get_height() - 30))


        self.imgBG = pygame.image.load('static/photo/bg_dialog_1.jpg')
        self.imgBG = pygame.transform.scale(self.imgBG, (self.window.get_width(), self.window.get_height()))
        self.imgMisato = pygame.image.load('static/photo/misato_ready.png')

    def draw(self):
        if not self.active: 
            return False


        self.window.blit(self.imgBG, (0, 0))
        misato_rect = self.imgMisato.get_rect(center=(self.window.get_width() // 8 * 6, self.window.get_height() // 5 * 3))
        self.window.blit(self.imgMisato, misato_rect)


        #self.dialog_surface.fill((0, 0, 0, 0))
        
        pygame.draw.rect(self.dialog_surface, self.background_color, (4, 4, self.width - 8, self.height - 8))
        pygame.draw.rect(self.dialog_surface, self.border_color, (0, 0, self.width, self.height), 4)
        

        self.window.blit(self.dialog_surface, (self.x, self.y))

        text_x = self.x + 30
        text_y = self.y + 15
        current_x = text_x
        current_y = text_y

        words = self.text.split(' ')
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
            pygame.draw.rect(self.window, pygame.Color('black'), self.menu_rect.inflate(10, 10), 3)
            return True
        return False