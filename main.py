from dialog_window import Dialog
from menu import Menu
import pygame
pygame.init()



WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

menu = Menu(window, 'start', 'info', '', 'exit')


play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.KEYDOWN:
            menu.event_handler(event)



    window.fill('black')

    menu.draw()



    clock.tick(FPS)
    pygame.display.update()        


pygame.quit()