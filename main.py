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

CURRENT_GAME_PROGRESS = None
with open ('static/data/saves.txt', 'r') as file:
    CURRENT_GAME_PROGRESS = int(file.read())
    print(CURRENT_GAME_PROGRESS)
MOUSE_CLICKED = False
SPACE_CLICKED = False
GAME_STATE = 'menu'
GAME_PHASE = ''
GAME_TYPE = 'speed_typing'
IS_MUSIC_PLAYING = False
MUSIC_MAKER = ''
#CURRENT_DIALOG = None
MENU = Menu(window, 'start', 'info', 'save/load', '' , 'exit')
Misato = Character('Misato', (222, 167, 255, 200), (209, 131, 255, 255), pygame.image.load('static/photo/misato.png'), (WIDTH // 2, HEIGHT // 5 * 4), (600, 1300))
Rei = Character('Rei', (148, 244, 255, 200), (59, 234, 255, 255), pygame.image.load('static/photo/rei.png'), (WIDTH // 8 * 6.2, HEIGHT // 5 * 3.42),(485, 900))
Asuka = Character('Asuka', (255, 113, 113, 200), (255, 63, 63, 255), pygame.image.load('static/photo/asuka.png'), (WIDTH // 8 * 1.5, HEIGHT // 5 * 3.8),(550, 1050))
CURRENT_DIALOG = Dialog(window,CURRENT_GAME_PROGRESS, Misato, Rei, Asuka)
INPUT_WORD = ''
TYPING_GAME = Speed_Typing(window)
ALPHA = 0          
FADE_SPEED = 10     
FADE_STATE = "out"
IS_BLACK_OUT = False


# def play_menu_music():
#     pygame.mixer.init()
#     pygame.mixer.music.load('static/music/opening.mp3')
#     pygame.mixer.music.play(-1)
#     pygame.mixer.music.set_volume(0.5)


def black_out():
    global ALPHA, FADE_SPEED, FADE_STATE

    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill('black')
    fade_surface.set_alpha(ALPHA)

    window.blit(fade_surface, (0, 0))

    if FADE_STATE == "out":
        ALPHA += FADE_SPEED
        if ALPHA >= 255:
            ALPHA = 255
            FADE_STATE = "in"  
    elif FADE_STATE == "in":
        ALPHA -= FADE_SPEED
        if ALPHA <= 0:
            ALPHA = 0
            FADE_STATE = "out"

    print("black")
    return ALPHA == 255

def change_state(input_data):
    global GAME_STATE
    global play
    global GAME_PHASE, IS_MUSIC_PLAYING
    print (input_data)
    match input_data:
        case 'exit':
            play = False
            pygame.mixer.music.pause()
            IS_MUSIC_PLAYING = False
        case 'start':
            GAME_STATE = 'game'
            GAME_PHASE = 'cutscene'
            pygame.mixer.music.pause()
            IS_MUSIC_PLAYING = False
        case 'info':
            GAME_STATE = 'info'
            print(GAME_STATE)
            pygame.mixer.music.pause()
            IS_MUSIC_PLAYING = False
        
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
    global GAME_STATE, MUSIC_MAKER, IS_MUSIC_PLAYING
    MUSIC_MAKER = 'menu'
    if not IS_MUSIC_PLAYING:
        music_turn_on(MUSIC_MAKER)
        IS_MUSIC_PLAYING = True
    MENU.draw()
    
def case_game():
    global GAME_PHASE, GAME_STATE, GAME_TYPE, SPACE_CLICKED, INPUT_WORD, MOUSE_CLICKED
    match GAME_PHASE:
                case 'game_process':
                    match GAME_TYPE:
                        case 'speed_typing':
                            case_speed_typing()
                case 'cutscene':
                    case_cutscene()
                        
def case_speed_typing():
    global GAME_PHASE, GAME_STATE, GAME_TYPE, SPACE_CLICKED, INPUT_WORD, MOUSE_CLICKED, TYPING_GAME, CURRENT_GAME_PROGRESS
    if not TYPING_GAME.active:
        returned = TYPING_GAME.initialize()
        if returned == 'menu' and MOUSE_CLICKED:
            GAME_PHASE = 'cutscene'
            GAME_STATE = 'menu'
            CURRENT_DIALOG.current_pos = 0
        
    elif TYPING_GAME.game_end:
        next_step = TYPING_GAME.end_window()
        match next_step:
            case 'menu':
                if MOUSE_CLICKED:
                    GAME_STATE = 'menu'
                    GAME_PHASE = 'cutscene'
                    CURRENT_DIALOG.current_pos = 0
                    TYPING_GAME.reset()
            case 'again':
                if MOUSE_CLICKED:
                    TYPING_GAME.reset()
                    INPUT_WORD = ''
            case 'continue':
                if MOUSE_CLICKED:
                    TYPING_GAME.reset()
                    INPUT_WORD = ''
                    CURRENT_GAME_PROGRESS += 1
                    CURRENT_DIALOG.game_progress = 1
                    CURRENT_DIALOG.update_data()
                    CURRENT_DIALOG.current_pos = 0
                    GAME_STATE = 'game'
                    GAME_PHASE = 'cutscene'
                    GAME_TYPE = ''
    else:
        match TYPING_GAME.play(INPUT_WORD.lower()):
            case True:
                INPUT_WORD = ''
            case 'menu':
                if MOUSE_CLICKED:
                    TYPING_GAME.reset()
            case _ : pass
    
def case_cutscene():
    global GAME_PHASE, GAME_STATE, GAME_TYPE, SPACE_CLICKED, INPUT_WORD, MOUSE_CLICKED, MUSIC_MAKER, IS_MUSIC_PLAYING

    MUSIC_MAKER = 'cutscene'
    if not IS_MUSIC_PLAYING:
        music_turn_on(MUSIC_MAKER)
        IS_MUSIC_PLAYING = True


    is_menu_press = CURRENT_DIALOG.draw()
    if is_menu_press and MOUSE_CLICKED:
        GAME_STATE = 'menu'
        pygame.mixer.music.pause()
        IS_MUSIC_PLAYING = False
        CURRENT_DIALOG.current_pos = 0
    if SPACE_CLICKED:
        if CURRENT_DIALOG.next():
            SPACE_CLICKED = False
        else:
            GAME_PHASE = 'game_process'
            pygame.mixer.music.pause()
            IS_MUSIC_PLAYING = False



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
        if GAME_STATE == 'menu' and event.type == pygame.KEYDOWN: change_state(MENU.event_handler(event))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: MOUSE_CLICKED = True 
        else : MOUSE_CLICKED = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: SPACE_CLICKED = True
        if event.type == pygame.KEYDOWN and GAME_PHASE == 'game_process' and not TYPING_GAME.active: TYPING_GAME.active = True
        if event.type == pygame.KEYDOWN and GAME_STATE == 'game' and GAME_PHASE == 'game_process' and GAME_TYPE == 'speed_typing': 
            if event.unicode.isalpha():
                INPUT_WORD += event.unicode
                print(INPUT_WORD)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE and GAME_STATE == 'game' and GAME_PHASE == 'game_process' and GAME_TYPE == 'speed_typing': 
            INPUT_WORD = INPUT_WORD[:-1]
            print(INPUT_WORD)


    window.fill(pygame.Color('black'))
    match GAME_STATE:
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





















