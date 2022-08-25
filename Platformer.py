from dis import dis
import pygame, sys, os, random, noise
import data.engine as e
import main_menu as mm
from settings import *
clock = pygame.time.Clock()

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() # initiates pygame
pygame.mixer.set_num_channels(64)

pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (1200,800)
game_font = pygame.font.SysFont( "arial", 30, True, False)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((600,400)) # used as the surface for rendering, which is scaled




        

def generate_chunk(x,y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE  + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0 # nothing
            height = 8 - int(noise.pnoise1(target_x * 0.1, repeat=999999) * 5)

             
            if target_y > height:
                tile_type = 2 # dirt
            elif target_y == height :
                tile_type = 1 # grass
            elif target_y == height - 1:
                num = random.randint(1,10)
                if num == 1:
                    tile_type = 3 # plant
                if num == 2:
                    tile_type = 5
            
            # elif target_y == height - 3:

            #     if random.randint(0, 10) == 0:
            #         tile_type = 1

            elif height - 12 < target_y < height - 8:
                if random.randint(1,50) == 1:
                    tile_type = 6
            elif target_y == height - 4:
                if random.randint(1,15) == 1:
                    tile_type = 4
            if tile_type != 0:
                chunk_data.append([[target_x,target_y],tile_type])
    return chunk_data


e.load_animations('data/images/entities/')





arrow_shoot_sound = pygame.mixer.Sound('data/audio/arrow.wav')
hit_sound = pygame.mixer.Sound('data/audio/hit.wav')
jump_sound = pygame.mixer.Sound('data/audio/jump.wav')
grass_sounds = [pygame.mixer.Sound('data/audio/grass_0.wav'),pygame.mixer.Sound('data/audio/grass_1.wav')]
arrow_shoot_sound.set_volume(0.2)
hit_sound.set_volume(0.2)
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load('data/audio/music.wav')
pygame.mixer.music.play(-1)


player = e.entity(100,0,10,26,'player')

# background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]



#for i in range(5):
#    spike_objects.append(e.spike((random.randint(0, 600)-300, 147)))

#for i in range(5):
#    jump_pole_objects.append(e.jump_pole((random.randint(0, 600)-300, 90)))

for i in range(3):
    enemies.append([0, e.entity(random.randint(player.x - 500, player.x - 400), random.randint(-100, -50), 15, 16, 'bunny'), 50])
    enemies.append([0, e.entity(random.randint(player.x + 400, player.x + 500), random.randint(-100, -50) , 15, 20, 'monkey'), 100])
    

mm.show_start_screen()

while True: # game loop
    clock.tick(60)
    display.fill((146,244,255)) # clear screen by filling it with blue
    
    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    true_scroll[0] += (player.x-true_scroll[0]-304)/20
    true_scroll[1] += (player.y-true_scroll[1]-212)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    #pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))

    """
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(20,170,150),obj_rect)
        else:
            pygame.draw.rect(display,(25,76,73),obj_rect)
    """

    tile_rects = []
    for y in range(3):
        for x in range(4):
            target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*16)))
            target_y = y - 1 + int(round(scroll[1]/(CHUNK_SIZE*16)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x,target_y)
            for tile in game_map[target_chunk]:
                display.blit(tile_index[tile[1]],(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1]))
                if tile[1] in [1,2]:
                    tile_rects.append(pygame.Rect(tile[0][0]*16,tile[0][1]*16,16,16))    

    # 이동
    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    
    
        


    # 이동 업데이트
    collision_types = player.move(player_movement, tile_rects)


    # 땅에서 걸을 때 잔디 소리
    if collision_types['bottom']:
        air_timer = 0
        vertical_momentum = 0
        if player_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer = 30
                random.choice(grass_sounds).play()
    else:
        air_timer += 1

    player.change_frame(1)
    player.display(display, scroll)

    if not enemies:
        for i in range(3):
            enemies.append([0, e.entity(random.randint(player.x - 500, player.x - 400), random.randint(-100, -50), 15, 16, 'bunny'), 50])
            enemies.append([0, e.entity(random.randint(player.x + 400, player.x + 500), random.randint(-100, -50), 15, 20, 'monkey'), 100])


    for enemy in enemies:
        enemy[0] += 0.2


        enemy_movement = [0, enemy[0]] 
        if enemy[1].action == 'idle':
            if player.x > enemy[1].x + 5:
                enemy_movement[0] = 1
                enemy[1].set_flip(True)
            if player.x < enemy[1].x - 5:
                enemy_movement[0] = -1
                enemy[1].set_flip(False)
        

        if enemy[1].y > 400: enemies.remove(enemy)
        collision_types = enemy[1].move(enemy_movement, tile_rects)
        if collision_types['bottom']:
             enemy[0] = 0
        if collision_types['right'] or collision_types['left']:
            enemy[0] = -4


        if enemy[1].action == 'die':
            if collision_types['bottom']:
                enemies.remove(enemy)
        
        if enemy[1].action == 'idle':

            if player.obj.rect.colliderect(enemy[1].obj.rect) and hit_cooldown == 0:
                if not game_over : hit_sound.play()
                current_health -= 3
                vertical_momentum = -4
                player_movement[0] += 4
                is_hitted = True
                hit_cooldown = 30

            for arrow in arrow_objects:
                if enemy[1].obj.rect.colliderect(arrow.get_rect()):

                    arrow_objects.remove(arrow)
                    enemy[2] -= arrow_offence_power


            if enemy[2] == 0:
                enemy[1].set_action('die')
                enemy[0] = -4
                
                score += 1

                if random.randint(0, 5) == 0:
                    meats.append([-3, e.entity(arrow.loc[0], arrow.loc[1], 16, 16, 'meat'), 0])
        
        
                

        
        
        
        # hp bar
        pygame.draw.rect(display, RED, (enemy[1].x - scroll[0] - 5, enemy[1].y - scroll[1] - 10, 20, 2))
        pygame.draw.rect(display, GREEN, (enemy[1].x - scroll[0] - 5, enemy[1].y - scroll[1] - 10, enemy[2] / 5, 2))
        enemy[1].change_frame(1)
        enemy[1].display(display, scroll)
    
    for meat in meats:
        meat[2] += 0.1

        if meat[2] >= 50: 
            meats.remove(meat)
        meat[0] += 0.1
        meat_movement = [0, meat[0]]

        collision_types = meat[1].move(meat_movement, tile_rects)
        
        if collision_types['bottom']: 
            meat[0] = 0

        if player.obj.rect.colliderect(meat[1].obj.rect):
            current_health += 30
            meats.remove(meat)

        meat[1].change_frame(1)
        meat[1].display(display, scroll)


    for arrow in arrow_objects:

        if arrow.flip == True:
            arrow.render(display, scroll, e.flip(arrow_img))
            arrow.loc[0] -= 3
        if arrow.flip == False:
            arrow.render(display, scroll, arrow_img)
            arrow.loc[0] += 3
            
            
    

        

        
        
    """

    for jump_pole in jump_pole_objects:
        jump_pole.render(display, scroll, jump_pole_img)
        if jump_pole.collision_test(player.obj.rect):
            vertical_momentum = -7

    for bullet in bullet_objects:
        bullet.render(display, scroll, bullet_img)
        if bullet.flip == True:
            bullet.loc[0] -= 3
        if bullet.flip == False:
            bullet.loc[0] += 3
        for spike in spike_objects:
            if bullet.collision_test(spike.get_rect()):
                bullet_objects.remove(bullet)
                spike_objects.remove(spike)

        for jump_pole in jump_pole_objects:
            if bullet.collision_test(jump_pole.get_rect()):
                bullet_objects.remove(bullet)


    for spike in spike_objects:
        spike.render(display, scroll, spike_img)
        if spike.collision_test(player.obj.rect):
            
    """


    if current_health <= 0: 
        game_over = True
        current_health = 0
    if current_health >= max_health:
        current_health = max_health

    if hit_cooldown > 0:
        hit_cooldown -= 1

    # 상태별 애니메이션
    if not game_over:

        if is_shooting_bullet == False and is_shooting_arrow == False and is_hitted == False:
            if player_movement[0] == 0:
                player.set_action('idle')
            if player_movement[0] > 0:
                player.set_flip(False)
                player.set_action('run')
            if player_movement[0] < 0:
                player.set_flip(True)
                player.set_action('run')
        if is_shooting_bullet:
            player.set_action('shoot')
            if player.animation_frame >= len(e.animation_higher_database['player']['shoot'][0]) - 1:
                is_shooting_bullet = False
        
        if is_shooting_arrow:
            player.set_action('arrow')
            if player.animation_frame >= len(e.animation_higher_database['player']['arrow'][0]) - 1:
                is_shooting_arrow = False
        
        elif is_hitted:
            player.set_action('hit')
            if player.animation_frame >= len(e.animation_higher_database['player']['hit'][0]) - 1:
                is_hitted = False

    if game_over:
        moving_right = False
        moving_left = False
        
        player.set_action('die')

        
        if player.animation_frame >= len(e.animation_higher_database['player']['die'][0]) - 1:
            if game_over_timer == 10 : 
                display.blit(game_over_img,(200,70))
            else : game_over_timer += 1

    

    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if game_over == False:
                if event.key == K_w:
                    pygame.mixer.music.fadeout(1000)
                if event.key == K_RIGHT:
                    moving_right = True
                if event.key == K_LEFT:
                    moving_left = True
                if event.key == K_UP:
                    if air_timer < 6:
                        jump_sound.play()
                        vertical_momentum = -5
                # if event.key == K_a:
                #     is_shooting_bullet = True
                #     bullet_objects.append(e.bullet([player.x + 10, player.y + 12], player.flip))
                if event.key == K_s:
                    is_shooting_arrow = True
                    arrow_shoot_sound.play()
                    arrow_objects.append(e.arrow([player.x + 6, player.y + 12], player.flip))
                    
            if game_over == True:
                
                
                if event.key == K_r:
                    game_over = False
                    
                    score = 0
                    current_health = 200
                    player = e.entity(100,0,10,26,'player')
                    enemies.clear()
                    arrow_objects.clear()
                    meats.clear()

                    for i in range(3):
                        enemies.append([0, e.entity(random.randint(player.x - 500, player.x - 400), random.randint(-100, -50), 15, 16, 'bunny'), 50])
                        enemies.append([0, e.entity(random.randint(player.x + 400, player.x + 500), random.randint(-100, -50), 15, 20, 'monkey'), 100])

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
    
    

    # hp bar
    pygame.draw.rect(display, RED, (10, 10, max_health, 5))
    pygame.draw.rect(display, GREEN, (10, 10, current_health, 5))

    score_board = game_font.render('score : ' + str(score), True, (255, 255, 255))
    
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    screen.blit(score_board, (10, 50))
    
    pygame.display.update()