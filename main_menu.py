import pygame
from data.engine import Font

pygame.mixer.pre_init(44100, -16, 2, 512)
clock = pygame.time.Clock()
WINDOW_SIZE = (1200,800)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window
frame_timer = 0
title_idx = 0

my_big_font = Font('data/font/large_font.png')
background_img = pygame.image.load('data/images/main_background.png')
title_images_base_path = 'data/images/title/game_title_'
title_images = []
for i in range(0, 10):
    title_images.append(pygame.image.load(title_images_base_path + str(i) + '.png'))

arrow_img = pygame.image.load('data/images/arrow.png')

click = False

def show_start_screen():
    
    global frame_timer, title_idx
    waiting = True
    while waiting:

        screen.blit(background_img,(0, 0))

        clock.tick(60)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(500, 630, 200, 50)
        button_2 = pygame.Rect(500, 680, 200, 50)
        button_3 = pygame.Rect(500, 730, 200, 50)

        if button_1.collidepoint((mx, my)):
            screen.blit(arrow_img, (420, 635))
            if click:
                story()
        if button_2.collidepoint((mx, my)):
            screen.blit(arrow_img, (420, 685))
            if click: 
                waiting = False
        if button_3.collidepoint((mx, my)):
            screen.blit(arrow_img, (420, 735))
            if click: 
                Help()

        pygame.draw.rect(screen, pygame.Color(255, 255, 255, 128), button_1)
        pygame.draw.rect(screen, pygame.Color(255, 255, 255, 128), button_2)
        pygame.draw.rect(screen, pygame.Color(255, 255, 255, 128), button_3)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        if frame_timer > 5: 
            frame_timer = 0 
            title_idx += 1
        else : frame_timer += 1

        if title_idx > len(title_images) - 1  : title_idx = 0
        my_big_font.render(screen, "Main Story", (525, 630))
        my_big_font.render(screen, "Start Game", (525, 680))
        my_big_font.render(screen, "Help", (570, 730))
        screen.blit(title_images[title_idx],(190, 120))
        
        pygame.display.update()
    
    
    pygame.display.flip()

    
        


def story():
    story_images_base_path = 'data/images/story/story_'
    story_idx = 0
    story_images = []
    for i in range(0, 5):
        story_images.append(pygame.image.load(story_images_base_path + str(i) + '.png'))
    running = True
    clock.tick(60)
    while running:
        
        screen.blit(story_images[story_idx], (0, 0))
        
        

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAFE:
                    running = False
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: story_idx += 1
        
        if story_idx > 4 : running = False
        pygame.display.update()


def Help():
    help_images_base_path = 'data/images/help/help_'
    help_idx = 0
    help_images = []
    for i in range(0, 2):
        help_images.append(pygame.image.load(help_images_base_path + str(i) + '.png'))
    running = True
    clock.tick(60)
    while running:

        screen.blit(help_images[help_idx], (200, 100))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAFE:
                    running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: help_idx += 1

        if help_idx > 1 : running = False
        
        pygame.display.update()
        


