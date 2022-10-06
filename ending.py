import pygame


pygame.mixer.pre_init(44100, -16, 2, 512)
clock = pygame.time.Clock()
WINDOW_SIZE = (1200,800)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window



def ending():
    ending_cooldown = 0
    ending_idx = 0
    ending_images_base_path = 'data/images/ending/ending_'
    ending_images = []
    for i in range(0, 7):
        ending_images.append(pygame.image.load(ending_images_base_path + str(i) + '.png'))
    running = True
    clock.tick(60)
    while running:
        screen.blit(ending_images[ending_idx], (0, 0))
        ending_cooldown += 1
        if ending_cooldown > 60: 
            if ending_idx != 6: 
                ending_cooldown = 0
                ending_idx += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ending_idx == 6 and event.button == 1: running = False
        pygame.display.update()
