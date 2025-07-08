import pygame

class Menu:
    def __init__(self,window, *args):
        self.points = args
        self.window = window
        self.itemFont = pygame.font.Font('static/fonts/main_font.otf', 40)
        self.selectFont_1 = pygame.font.Font('static/fonts/main_font.otf', 55)
        self.selectFont_2 = pygame.font.Font('static/fonts/main_font.otf', 45)
        self.select = 0
        self.timer = 0
        self.selectAdd = 0
        self.timer = 0
        self.imgBG = pygame.image.load('static/photo/bg_menu.jpg')
        self.imgBG = pygame.transform.scale(self.imgBG, (self.window.get_width(), self.window.get_height()))


    def draw(self):
        self.window.blit(self.imgBG, (0, 0))
        self.timer = (self.timer + 1) % 60
        for i in range(len(self.points)):
            if i == self.select:
                if self.timer < 30:
                    text = self.selectFont_1.render(self.points[i], 1, (255, 179, 179))
                else:
                    text = self.selectFont_2.render(self.points[i], 1, (255, 179, 179))
            else:
                text = self.itemFont.render(self.points[i], 1, (201, 141, 255))
            posX = self.window.get_width() // 2
            posY = self.window.get_height() // 2 - 150 + 50 * i
            rect = text.get_rect(center = (posX, posY))
            self.window.blit(text, rect)


    def event_handler(self, event):
        print(f"Key pressed: {event.key}")  # Проверьте, что K_RETURN/K_SPACE срабатывают
        if event.key == pygame.K_UP: self.selectAdd -= 1
        if event.key == pygame.K_DOWN: self.selectAdd += 1 

        self.select = (self.select + self.selectAdd) % len(self.points)

        while self.points[self.select] == '':
            self.select = (self.select + self.selectAdd) % len(self.points)

        self.selectAdd = 0

        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
            if self.points[self.select] == "exit": return 'exit'
            if self.points[self.select] == "info": return 'info'
            if self.points[self.select] == "start": return 'start'