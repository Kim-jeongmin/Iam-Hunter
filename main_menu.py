import pygame

pygame.mixer.pre_init(44100, -16, 2, 512)
clock = pygame.time.Clock()
WINDOW_SIZE = (1200,800)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window
frame_timer = 0
title_idx = 0

title_images_base_path = 'data/images/title/game_title_'
title_images = []
for i in range(0, 10):
    title_images.append(pygame.image.load(title_images_base_path + str(i) + '.png'))


def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, 40)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    
    screen.blit(text_surface, text_rect)    

def show_start_screen():
    
    
    
    global frame_timer, title_idx
    waiting = True
    while waiting:
        screen.fill((0,0,0))
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    waiting = False
        
        if frame_timer > 5: 
            frame_timer = 0 
            title_idx += 1
        else : frame_timer += 1

        if title_idx > len(title_images) - 1  : title_idx = 0
        draw_text("Press any key to play", 22, (255, 255, 255), 600, 800-150)
        screen.blit(title_images[title_idx],(190, 50))
        pygame.display.update()
    
    
    pygame.display.flip()
    
        

