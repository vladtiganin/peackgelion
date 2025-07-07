from dialog_window import Dialog
import pygame
pygame.init()


WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False


    dia = Dialog(window, 'The quick brown fox jumps over the lazy dog. This sentence contains all 26 letters of the English alphabet. Numbers test: 1234567890. Special characters: !#$%^&*()_+-=[]{};,./<>? Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl eget ultricies tincidunt, nisl nisl aliquam nisl, eget ultricies nisl nisl eget nisl.')

    dia.draw()
    



    clock.tick(FPS)
    pygame.display.update()        


pygame.quit()