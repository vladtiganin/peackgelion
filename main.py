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



WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60


'''
game_state:     1) menu - на экране меню и там
                2) game - сам игровой процесс
                3) cutscene - катсцена
                4) найстройки или меню сохранения надо придумать 
'''



game_state = 'menu'
game_phase = ''
menu = Menu(window, 'start', 'info', '', 'exit')


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
            match game_phase:
                case 'game_process':
                    pass
                case 'cutscene':
                    dialog = Dialog(window, "Longer paragraph to test word wrapping and text formatting capabilities. The rain in Spain stays mainly in the plain. How now brown cow. She sells seashells by the seashore.Final line with punctuation! Question? Yes. Done.")
                    dialog.draw()
        case 'settings':
            pass
        case 'save':
            pass



    clock.tick(FPS)
    pygame.display.update()        


pygame.quit()