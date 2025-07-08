from dialog_window import Dialog
from menu import Menu
from character import Character
from speed_typing import Speed_Typing
import pygame
from random import randint


pygame.init()


info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
# WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 60


mouse_clicked = False
space_clicked = False
game_state = 'menu'
game_phase = ''
game_type = 'speed_typing'
current_dialog = None
menu = Menu(window, 'start', 'info', 'save/load', '' , 'exit')
Misato = Character('Misato', (222, 167, 255, 200), (209, 131, 255, 255), pygame.image.load('static/photo/misato_ready.png'), (WIDTH // 2, HEIGHT // 5 * 3))
Rei = Character('Rei', (148, 244, 255, 200), (59, 234, 255, 255), pygame.image.load('static/photo/rei_dress-up.png'), (WIDTH // 8 * 6, HEIGHT // 5 * 3))
Asuka = Character('Asuka', (255, 113, 113, 200), (255, 63, 63, 255), pygame.image.load('static/photo/asuka_dress-up.png'), (WIDTH // 8 * 2, HEIGHT // 5 * 3))
current_dialog = Dialog(window, 'static/data/introduction.txt', Misato, Rei, Asuka)
input_word = ''
typing = Speed_Typing(window)


def change_state(input_data):
    global game_state
    global play
    global game_phase
    print (input_data)
    match input_data:
        case 'exit':
            play = False
        case 'start':
            game_state = 'game'
            game_phase = 'cutscene'
        case 'info':
            game_state = 'info'
            print(game_state)

def case_menu():
    global game_state
    if menu.draw():
        game_state = 'menu'

def case_game():
    global game_phase, game_state, game_type, space_clicked, input_word, mouse_clicked
    match game_phase:
                case 'game_process':
                    match game_type:
                        case 'speed_typing':
                            case_speed_typing()
                case 'cutscene':
                    case_cutscene()

def case_speed_typing():
    global game_phase, game_state, game_type, space_clicked, input_word, mouse_clicked, typing
    if not typing.active:
        returned = typing.initialize()
        if returned == 'menu' and mouse_clicked:
            game_phase = 'cutscene'
            game_state = 'menu'
            current_dialog.current_pos = 0
        
    elif typing.game_end:
        next_step = typing.end_window()
        match next_step:
            case 'menu':
                if mouse_clicked:
                    game_state = 'menu'
                    typing.reset()
    else:
        match typing.play(input_word.lower()):
            case True:
                input_word = ''
            case 'menu':
                if mouse_clicked:
                    typing.reset()
            case _ : pass
    
def case_cutscene():
    global game_phase, game_state, game_type, space_clicked, input_word, mouse_clicked
    is_menu_press = current_dialog.draw()
    if is_menu_press and mouse_clicked:
        game_state = 'menu'
    if space_clicked:
        if current_dialog.next():
            space_clicked = False
        else:
            game_phase = 'game_process'



'''
game_state:     1) menu - на экране меню и там
                2) game - сам игровой процесс
                3) cutscene - катсцена
                4) найстройки или меню сохранения надо придумать 
'''


play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if game_state == 'menu' and event.type == pygame.KEYDOWN: change_state(menu.event_handler(event))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: mouse_clicked = True 
        else : mouse_clicked = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: space_clicked = True
        if event.type == pygame.KEYDOWN and game_phase == 'game_process' and not typing.active: typing.active = True
        if event.type == pygame.KEYDOWN and game_state == 'game' and game_phase == 'game_process' and game_type == 'speed_typing': 
            if event.unicode.isalpha():
                input_word += event.unicode
                print(input_word)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE and game_state == 'game' and game_phase == 'game_process' and game_type == 'speed_typing': 
            input_word = input_word[:-1]
            print(input_word)


    window.fill(pygame.Color('black'))

    match game_state:
        case 'menu':
            case_menu()
        case 'game':
            case_game()
        case 'settings':
            pass
        case 'save':
            pass


    clock.tick(FPS)
    pygame.display.update()        


pygame.quit()





















