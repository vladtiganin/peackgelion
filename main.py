from dialog_window import Dialog
from menu import Menu
import pygame
pygame.init()

def change_state(input_data):
    global game_state
    global play
    global game_phase
    print ('change_state')
    match input_data:
        case 'exit':
            play = False
        case 'start':
            game_state = 'game'
            game_phase = 'cutscene'
        case 'info':
            game_state = 'info'
            print(game_state)


info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
# WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 60


'''
game_state:     1) menu - на экране меню и там
                2) game - сам игровой процесс
                3) cutscene - катсцена
                4) найстройки или меню сохранения надо придумать 
'''


mouse_clicked = False
game_state = 'menu'
game_phase = ''
menu = Menu(window, 'start', 'info', '', 'exit')


play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if game_state == 'menu' and event.type == pygame.KEYDOWN: change_state(menu.event_handler(event))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: mouse_clicked = True 
        else : mouse_clicked = False



    window.fill(pygame.Color('black'))
    match game_state:
        case 'menu':
            if menu.draw():
                game_state = 'menu'
        case 'game':
            match game_phase:
                case 'game_process':
                    pass
                case 'cutscene':
                    dialog = Dialog(window, 'Please, eat my horny pussy...')
                    is_left_button_press = dialog.draw()
                    if is_left_button_press and mouse_clicked:
                        game_state = 'menu'
        case 'settings':
            pass
        case 'save':
            pass



    clock.tick(FPS)
    pygame.display.update()        


pygame.quit()