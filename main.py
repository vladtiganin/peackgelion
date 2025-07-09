from dialog_window import Dialog
from menu import Menu
from character import Character
from speed_typing import Speed_Typing
import pygame
from random import randint


pygame.init()

pygame.mixer.init()
# pygame.mixer.music.play(-1)
# pygame.mixer.music.set_volume(0.5)
# pygame.mixer.music.unpause()

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
is_music_playing = False
music_maker = ''
current_dialog = None
menu = Menu(window, 'start', 'info', 'save/load', '' , 'exit')
Misato = Character('Misato', (222, 167, 255, 200), (209, 131, 255, 255), pygame.image.load('static/photo/misato.png'), (WIDTH // 2, HEIGHT // 5 * 4), (600, 1300))
Rei = Character('Rei', (148, 244, 255, 200), (59, 234, 255, 255), pygame.image.load('static/photo/rei.png'), (WIDTH // 8 * 6.2, HEIGHT // 5 * 3.42),(485, 900))
Asuka = Character('Asuka', (255, 113, 113, 200), (255, 63, 63, 255), pygame.image.load('static/photo/asuka.png'), (WIDTH // 8 * 1.5, HEIGHT // 5 * 3.8),(550, 1050))
current_dialog = Dialog(window, 'static/data/introduction.txt', Misato, Rei, Asuka)
input_word = ''
typing = Speed_Typing(window)
alpha = 0          
fade_speed = 10     
fade_state = "out"
is_black_out = False



# def play_menu_music():
#     pygame.mixer.init()
#     pygame.mixer.music.load('static/music/opening.mp3')
#     pygame.mixer.music.play(-1)
#     pygame.mixer.music.set_volume(0.5)


def black_out():
    global alpha, fade_speed, fade_state

    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill('black')
    fade_surface.set_alpha(alpha)

    window.blit(fade_surface, (0, 0))

    if fade_state == "out":
        alpha += fade_speed
        if alpha >= 255:
            alpha = 255
            fade_state = "in"  
    elif fade_state == "in":
        alpha -= fade_speed
        if alpha <= 0:
            alpha = 0
            fade_state = "out"

    print("black")
    return alpha == 255


def change_state(input_data):
    global game_state
    global play
    global game_phase, is_music_playing
    print (input_data)
    match input_data:
        case 'exit':
            play = False
            pygame.mixer.music.pause()
            is_music_playing = False
        case 'start':
            game_state = 'game'
            game_phase = 'cutscene'
            pygame.mixer.music.pause()
            is_music_playing = False
        case 'info':
            game_state = 'info'
            print(game_state)
            pygame.mixer.music.pause()
            is_music_playing = False
        
    # pygame.mixer.music.pause()
    # is_music_playing = False

def music_turn_on(music_maker):
    match music_maker:
        case 'menu':
            pygame.mixer.music.load('static/music/opening.mp3')
        case 'cutscene':
            pygame.mixer.music.load('static/music/cutscene.mp3')

    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.unpause()

def case_menu():
    global game_state, music_maker, is_music_playing
    music_maker = 'menu'
    if not is_music_playing:
        music_turn_on(music_maker)
        is_music_playing = True
    menu.draw()
    
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
                    game_phase = 'cutscene'
                    current_dialog.current_pos = 0
                    typing.reset()
            case 'again':
                if mouse_clicked:
                    typing.reset()
                    input_word = ''
    else:
        match typing.play(input_word.lower()):
            case True:
                input_word = ''
            case 'menu':
                if mouse_clicked:
                    typing.reset()
            case _ : pass
    
def case_cutscene():
    global game_phase, game_state, game_type, space_clicked, input_word, mouse_clicked, music_maker, is_music_playing

    music_maker = 'cutscene'
    if not is_music_playing:
        music_turn_on(music_maker)
        is_music_playing = True


    is_menu_press = current_dialog.draw()
    if is_menu_press and mouse_clicked:
        game_state = 'menu'
        pygame.mixer.music.pause()
        is_music_playing = False
        current_dialog.current_pos = 0
    if space_clicked:
        if current_dialog.next():
            space_clicked = False
        else:
            game_phase = 'game_process'
            pygame.mixer.music.pause()
            is_music_playing = False



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


    #window.fill(pygame.Color('black'))

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





















