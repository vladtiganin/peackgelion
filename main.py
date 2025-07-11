from dialog_window import Dialog
from menu import Menu
from character import Character
from speed_typing import Speed_Typing
from end_game import End_Game
import pygame
from random import randint
from FirstLevel import FirstLevel


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
with open ('static/data/save.txt', 'r') as file:
    CURRENT_GAME_PROGRESS = int(file.read())
    print(CURRENT_GAME_PROGRESS)
MOUSE_CLICKED = False
SPACE_CLICKED = False
GAME_STATE = 'menu'
GAME_PHASE = ''
GAME_TYPE = ''
IS_MUSIC_PLAYING = False
MUSIC_MAKER = ''
#CURRENT_DIALOG = None
MENU = Menu(window, 'continue', '', 'new game', '' , 'exit')
Misato = Character('Misato', 
                   (222, 167, 255, 200), 
                   (209, 131, 255, 255), 
                   (WIDTH // 2, HEIGHT // 5 * 4),
                    imgs = (
                        {
                        'img' : pygame.image.load('static/photo/misato_1.png'),
                        'size' : (600, 1300)
                     },
                     {
                         'img' : pygame.image.load('static/photo/misato_2.png'),
                        'size' : (485, 1300)
                     }
                    ))
Rei = Character('Rei', 
                (148, 244, 255, 200), 
                (59, 234, 255, 255), 
                (WIDTH // 8 * 6.2, HEIGHT // 5 * 3.42),
                imgs = (
                    {
                        'img' : pygame.image.load('static/photo/rei_1.png'),
                        'size' : (485, 900)
                     },
                     {
                         'img' : pygame.image.load('static/photo/rei_2.png'),
                        'size' : (485, 900)
                     }
                ))

Asuka = Character('Asuka', 
                  (255, 113, 113, 200), 
                  (255, 63, 63, 255), 
                  (WIDTH // 8 * 1.5, HEIGHT // 5 * 3.8),
                    imgs = (
                        {
                        'img' : pygame.image.load('static/photo/asuka_1.png'),
                        'size' : (550, 1050)
                     },
                     {
                         'img' : pygame.image.load('static/photo/asuka_2.png'),
                        'size' : (550, 1050)
                     }
                    ))
CURRENT_DIALOG = Dialog(window,CURRENT_GAME_PROGRESS, Misato, Rei, Asuka)
INPUT_WORD = ''
TYPING_GAME = Speed_Typing(window)
END_GAME = End_Game(window)
ALPHA = 0          
FADE_SPEED = 10     
FADE_STATE = "out"
IS_BLACK_OUT = False
RETURNED_UNIT = None
TYPING_SOUND = pygame.mixer.Sound('static/music/typing_sound.wav')
FIRST_LEVEL = FirstLevel(window)

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
    global PLAY
    global GAME_PHASE, IS_MUSIC_PLAYING, CURRENT_GAME_PROGRESS, SPACE_CLICKED
    SPACE_CLICKED = False
    print (input_data)
    match input_data:
        case 'exit':
            PLAY = False
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
        case 'new game':
            CURRENT_GAME_PROGRESS = 0
            with open('static/data/save.txt', 'w') as file:
                file.write('0')
                change_state('start')

        
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
                        case 'end_game':
                            case_end_game()
                        case 'First level':
                            case_first_level()
                case 'cutscene':
                    case_cutscene()

def case_first_level():
    global GAME_PHASE, GAME_STATE, GAME_TYPE, SPACE_CLICKED, INPUT_WORD, MOUSE_CLICKED, TYPING_GAME, CURRENT_GAME_PROGRESS, END_GAME
    returned = FIRST_LEVEL.run()
    if returned == "menu":
        GAME_STATE = "menu"
        GAME_PHASE = "cutscene"
    elif returned == "continue":
        CURRENT_GAME_PROGRESS += 1
        CURRENT_DIALOG.game_progress += 1
        CURRENT_DIALOG.update_data()
        CURRENT_DIALOG.current_pos = 0
        GAME_STATE = "game"
        GAME_PHASE = "cutscene"
        GAME_TYPE = ""
        SPACE_CLICKED = False
        CURRENT_DIALOG.need_new_img = True
        with open("static/data/save.txt", "w") as file:
            file.write(str(CURRENT_GAME_PROGRESS))

def case_end_game():
    global GAME_PHASE, GAME_STATE, GAME_TYPE, SPACE_CLICKED, INPUT_WORD, MOUSE_CLICKED, TYPING_GAME, CURRENT_GAME_PROGRESS, END_GAME
    if not END_GAME.active:
        returned = END_GAME.initialize()
        if returned == 'menu' and MOUSE_CLICKED:
            GAME_PHASE = 'cutscene'
            GAME_STATE = 'menu'
            CURRENT_DIALOG.current_pos = 0

    elif END_GAME.is_end:
        next_step = END_GAME.game_end()
        match next_step:
            case 'menu':
                if MOUSE_CLICKED:
                    GAME_STATE = 'menu'
                    GAME_PHASE = 'cutscene'
                    CURRENT_DIALOG.current_pos = 0
                    END_GAME.reset()
            case 'again':
                if MOUSE_CLICKED:
                    END_GAME.reset()
            case 'continue':
                if MOUSE_CLICKED:
                    END_GAME.reset()
                    CURRENT_GAME_PROGRESS += 1
                    CURRENT_DIALOG.game_progress += 1
                    CURRENT_DIALOG.update_data()
                    CURRENT_DIALOG.current_pos = 0
                    GAME_STATE = 'game'
                    GAME_PHASE = 'cutscene'
                    GAME_TYPE = ''
                    SPACE_CLICKED = False
                    with open('static/data/save.txt', 'w') as file:
                        file.write(str(CURRENT_GAME_PROGRESS))

    else:
        RETURNED_UNIT = END_GAME.play()
        match RETURNED_UNIT:
            case 'menu':
                if MOUSE_CLICKED:
                    GAME_PHASE = 'cutscene'
                    GAME_STATE = 'menu'
                    CURRENT_DIALOG.current_pos = 0  
                    END_GAME.reset()
            # case 'select':
            #     if MOUSE_CLICKED:
            #         END_GAME.select = True
            # case _ : 
            #     END_GAME.select = False
                
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
                    SPACE_CLICKED = False
                    with open('static/data/save.txt', 'w') as file:
                        file.write(str(CURRENT_GAME_PROGRESS))
    else:
        match TYPING_GAME.play(INPUT_WORD.lower()):
            case True:
                INPUT_WORD = ''
            case 'menu':
                if MOUSE_CLICKED:
                    TYPING_GAME.reset()
            case _ : pass
    
def case_cutscene():
    global GAME_PHASE, GAME_STATE, GAME_TYPE, SPACE_CLICKED, INPUT_WORD, MOUSE_CLICKED, MUSIC_MAKER, IS_MUSIC_PLAYING, CURRENT_GAME_PROGRESS

    MUSIC_MAKER = 'cutscene'
    if not IS_MUSIC_PLAYING:
        music_turn_on(MUSIC_MAKER)
        IS_MUSIC_PLAYING = True

    CURRENT_DIALOG.game_progress = CURRENT_GAME_PROGRESS
    CURRENT_DIALOG.update_data()


    is_menu_press = CURRENT_DIALOG.draw()
    if is_menu_press and MOUSE_CLICKED:
        GAME_STATE = 'menu'
        pygame.mixer.music.pause()
        IS_MUSIC_PLAYING = False
        CURRENT_DIALOG.current_pos = 0
    if SPACE_CLICKED:
        if CURRENT_DIALOG.next():
            SPACE_CLICKED = False
            CURRENT_DIALOG.need_new_img = True
            SPACE_CLICKED = False
        else:
            if CURRENT_GAME_PROGRESS == 3:
                CURRENT_GAME_PROGRESS = 0
                with open('static/data/save.txt', 'w') as file:
                    file.write('0')
                    change_state('menu')
                    MOUSE_CLICKED = False
                    SPACE_CLICKED = False
                    GAME_STATE = 'menu'
                    GAME_PHASE = ''
                    GAME_TYPE = ''
                    IS_MUSIC_PLAYING = False
                    MUSIC_MAKER = ''
                    CURRENT_DIALOG.update_data()
                    CURRENT_DIALOG.current_pos = 0

            else:
                GAME_PHASE = 'game_process'
                CURRENT_DIALOG.need_new_img = True
                define_game()
                pygame.mixer.music.pause()
                IS_MUSIC_PLAYING = False

def define_game():
    global GAME_TYPE
    match CURRENT_GAME_PROGRESS:
        case 0: GAME_TYPE = 'First level'
        case 2: GAME_TYPE = 'end_game'
        case 1: GAME_TYPE = 'speed_typing'
    



PLAY = True
while PLAY:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            PLAY = False
        if GAME_STATE == 'menu' and event.type == pygame.KEYDOWN: change_state(MENU.event_handler(event))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: MOUSE_CLICKED = True 
        else : MOUSE_CLICKED = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and GAME_STATE == 'game' and GAME_PHASE == 'game_process' and GAME_TYPE == 'end_game' and END_GAME.active == True: 
            END_GAME.check_for_select()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: SPACE_CLICKED = True
        if event.type == pygame.KEYDOWN and GAME_PHASE == 'game_process' and not TYPING_GAME.active: TYPING_GAME.active = True
        if event.type == pygame.KEYDOWN and GAME_PHASE == 'game_process' and not END_GAME.active: END_GAME.active = True
        if event.type == pygame.KEYDOWN and GAME_STATE == 'game' and GAME_PHASE == 'game_process' and GAME_TYPE == 'speed_typing': 
            if event.unicode.isalpha():
                TYPING_SOUND.play()
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





















