import pygame

class Character:
    def __init__(self, name, background_color, border_color, img, position, size):
        self.position = position
        self.name = name
        self.background_color = background_color
        self.border_color = border_color
        self.width, self.height = size[0], size[1]
        self.img = pygame.transform.smoothscale(img, (size[0], size[1]))

    
    