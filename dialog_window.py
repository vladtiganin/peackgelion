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

        self.background_color = pygame.Color(255, 195, 27)
        self.border_color = pygame.Color(230, 169, 0)
        self.text_color = pygame.Color('black')
        self.text_font = pygame.font.SysFont('Arial', 20)


    def activate(self): 
        self.activate = True
        return True
    

    def diactivate(self): 
        self.activate = False
        return False


    def draw(self):
        if not self.active: return

        pygame.draw.rect(self.window, self.background_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.window, self.border_color, (self.x - 4, self.y - 4, self.width + 8, self.height + 8), 4)

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
