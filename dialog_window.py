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

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        self.background_color = pygame.Color(255, 195, 27)
        self.border_color = pygame.Color(230, 169, 0)
        self.text_color = pygame.Color('black')
        self.text_font = pygame.font.SysFont('static/fonts/main_font.otf', 37)

        self.menu_font = pygame.font.Font('static/fonts/main_font.otf', 20)
        self.menu_text = self.menu_font.render('Menu', True, 'black')
        self.menu_rect =  self.menu_text.get_rect(bottomright = (120, self.window.get_height() - 30))

        self.imgBG = pygame.image.load('static/photo/bg_dialog_1.jpg')
        self.imgBG = pygame.transform.scale(self.imgBG, (self.window.get_width(), self.window.get_height()))



    # def activate(self): 
    #     self.activate = True
    #     return True
    

    # def diactivate(self): 
    #     self.activate = False
    #     return False


    def draw(self):
        if not self.active: return

        self.window.blit(self.imgBG, (0, 0)) 

        self.imgMisato = pygame.image.load('static/photo/misato_ready.png')
        rect = self.imgMisato.get_rect(center = (self.window.get_width() // 8 * 6, self.window.get_height() // 5 * 3)) 
        self.window.blit(self.imgMisato, rect)

        pygame.draw.rect(self.window, self.background_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.window, self.border_color, (self.x - 8, self.y - 8, self.width + 16, self.height + 16), 4)
        pygame.draw.rect(self.window, 'black', (self.x - 4, self.y - 4, self.width + 8, self.height + 8), 4)


        text_x = self.x + 30
        text_y = self.y + 15
        curentXpos = text_x
        currentYpos = text_y
        line_spacing = 25

        words = self.text.split(' ')
        for word in words:
            word = self.text_font.render(word + ' ', 1, self.text_color)
            if word.get_width() > self.width - curentXpos + 50:
                currentYpos += word.get_height() + 5
                curentXpos = text_x

            self.window.blit(word , (curentXpos, currentYpos))
            curentXpos += word.get_width()

        

        self.window.blit(self.menu_text, self.menu_rect)  

        mouseX, mouseY = pygame.mouse.get_pos()
        if self.menu_rect.collidepoint((mouseX, mouseY)):
            border_rect = self.menu_rect.inflate(10, 10)
            pygame.draw.rect(self.window, pygame.Color('black'), border_rect, 3)
            return True
        return False
