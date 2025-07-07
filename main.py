from dialog_window import Dialog
from menu import Menu
import pygame
pygame.init()

def change_state(input_data):
    global play
    match input_data:
        case 'exit':
            play = False
        case _:
            print(input_data)



WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60


'''
game_state:     1) menu - на экране меню и там
                2) game - сам игровой процесс
                3) найстройки или меню сохранения надо придумать 
'''

game_state = 'menu'
menu = Menu(window, 'start', 'info', '', 'exit')

# global play
play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if game_state == 'menu' and event.type == pygame.KEYDOWN:
            change_state(menu.event_handler(event))

    window.fill(pygame.Color('black'))
    match game_state:
        case 'menu':
            menu.draw()
        case 'game':
            pass
        case 'settings':
            pass
        case 'save':
            pass



    clock.tick(FPS)
    pygame.display.update()        


pygame.quit()