import pygame

class Menu:
    def __init__(self,window, *args):
        self.points = args
        self.window = window
        self.itemFont = pygame.font.Font(None, 40)
        self.selectFont = pygame.font.Font(None, 55)
        self.select = 0
        self.timer = 0
        self.selectAdd = 0
        self.timer = 0


    def draw(self):
        self.timer = (self.timer + 1) % 60
        for i in range(len(self.points)):
            if i == self.select and self.timer < 30:
                text = self.selectFont.render(self.points[i], 1, (255, 179, 179))
            else:
                text = self.itemFont.render(self.points[i], 1, (201, 141, 255))
            rect = text.get_rect(center = (self.window.get_width() // 2, 100 + 50 * i))
            self.window.blit(text, rect)


    def event_handler(self, event):
        print(f"Key pressed: {event.key}")  # Проверьте, что K_RETURN/K_SPACE срабатывают
        global play
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