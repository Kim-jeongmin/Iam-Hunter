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
                num = random.randint(1,20)
                if num == 1:
                    tile_type = 3 # plant
                if num == 2:
                    tile_type = 5
            
            elif target_y == height - 3:

                if random.randint(0, 10) == 0:
                    tile_type = 4

            elif height - 12 < target_y < height - 8:
                if random.randint(1,50) == 1:
                    tile_type = 6
            #elif target_y == height - 3:
            #    if random.randint(1,15) == 1:
            #        tile_type = 4
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






player = e.entity(100,0,10,26,'player')





#for i in range(5):
#    spike_objects.append(e.spike((random.randint(0, 600)-300, 147)))

#for i in range(5):
#    jump_pole_objects.append(e.jump_pole((random.randint(0, 600)-300, 90)))

for i in range(2):
    enemies.append([0, e.entity(random.randint(player.x - 500, player.x - 400), random.randint(-100, -50), 15, 16, 'bunny'), 50])
    enemies.append([0, e.entity(random.randint(player.x + 400, player.x + 500), random.randint(-100, -50) , 15, 20, 'monkey'), 100])
    
mm.show_start_screen()

pygame.mixer.music.load('data/audio/noon.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)


while True: # game loop
    clock.tick(60)
    if game_time <= 1200 : 
        
        display.fill((146,244,255)) # clear screen by filling it with blue
        is_night = False
    elif 1200 < game_time <= 1300: display.fill((243,138,110)) 
    elif 1300 < game_time <= 1400: 
        display.fill((201,109,127))
        # pygame.mixer.music.fadeout(2000)
    elif 1400 < game_time <= 1500: display.fill((125,94,128))
    elif 1500 < game_time <= 1600: display.fill((87,68,111))
    else: 
        display.fill((19,26,98))
        is_night = True
    

    game_time += 1
    if game_time >= 3000: 
        game_time = 0
        days += 1
    
    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    true_scroll[0] += (player.x-true_scroll[0]-304)/20
    true_scroll[1] += (player.y-true_scroll[1]-212)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])




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
        if enemy[1].action == 'rage':
            if player.x > enemy[1].x + 5:
                enemy_movement[0] = 2
                enemy[1].set_flip(True)
            if player.x < enemy[1].x - 5:
                enemy_movement[0] = -2
                enemy[1].set_flip(False)
        
        if is_night and enemy[1].action == 'idle':
            enemy[1].set_action('rage')
        if not is_night and enemy[1].action == 'rage':
            enemy[1].set_action('idle')

        if enemy[1].y > 400: enemies.remove(enemy)
        collision_types = enemy[1].move(enemy_movement, tile_rects)
        if collision_types['bottom']:
             enemy[0] = 0
        if collision_types['right'] or collision_types['left']:
            enemy[0] = -4


        if enemy[1].action == 'die':
            if collision_types['bottom']:
                enemies.remove(enemy)
        
        if enemy[1].action == 'idle' or enemy[1].action == 'rage':

            if player.obj.rect.colliderect(enemy[1].obj.rect) and hit_cooldown == 0:
                if not game_over : 
                    hit_sound.play()
                    vertical_momentum = -4
                current_health -= 3 + days
                player_movement[0] += 4
                is_hitted = True
                hit_cooldown = 30

            for arrow in arrow_objects:
                if enemy[1].obj.rect.colliderect(arrow[1].obj.rect) and arrow[1].action == 'idle':

                    arrow_objects.remove(arrow)
                    enemy[2] -= arrow_offence_power
                    
                    if arrow[0] == True: 
                        enemy[1].x -= 2
                    elif arrow[0] == False:
                        enemy[1].x += 2

            if enemy[2] <= 0:
                enemy[1].set_action('die')
                enemy[0] = -4
                
                score += 1

                if random.randint(0, 5) == 0:
                    meats.append([-2, e.entity(enemy[1].x, enemy[1].y, 16, 16, 'meat'), 0])
        
        if enemy[1].action == 'hit':
            if enemy[1].animation_frame >= len(e.animation_higher_database['monkey']['hit'][0]) - 1:
                enemy[1].set_action('idle')
        
                

        
        
        
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

    for c in club:
        
        if player.flip == True:
            c[0].x = player.x - 12
            c[0].y = player.y - 10
            c[0].obj.rect.x = player.x - 12
            c[0].obj.rect.y = player.y - 10
            c[0].set_flip(True)
        elif player.flip == False:
            c[0].x = player.x 
            c[0].y = player.y - 10
            c[0].obj.rect.x = player.x
            c[0].obj.rect.y = player.y - 10
            c[0].set_flip(False)

        for enemy in enemies:
            if enemy[1].obj.rect.colliderect(c[0].obj.rect):
                if enemy[1].action == 'idle' or enemy[1].action == 'rage':
                    enemy[2] -= 30
                enemy[1].set_action('hit')
                
                if player.flip == False:
                    enemy[1].x += 5
                else :
                    enemy[1].x -= 5

        c[0].change_frame(1)
        c[0].display(display, scroll)

    for arrow in arrow_objects:
        
        
        
            
        arrow_movement = [0, 0]    
            
        if arrow[0] == False:
            arrow[1].set_flip(False)
            arrow_movement[0] += 3
        if arrow[0] == True:
            arrow[1].set_flip(True)
            arrow_movement[0] -= 3
       
        collision_types = arrow[1].move(arrow_movement, tile_rects)
        
        if collision_types['right'] or collision_types['left']:
            arrow[1].set_action('die')

        if player.obj.rect.colliderect(arrow[1].obj.rect) : 
            arrow_objects.remove(arrow)
            arrow_cnt += 1

        arrow[1].change_frame(1)
        arrow[1].display(display, scroll)
            
            
            
    

        

        
        
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

        if is_wielding_club == False and is_shooting_arrow == False and is_hitted == False:
            if player_movement[0] == 0:
                player.set_action('idle')
            if player_movement[0] > 0:
                player.set_flip(False)
                player.set_action('run')
            if player_movement[0] < 0:
                player.set_flip(True)
                player.set_action('run')
        if is_wielding_club:
            player.set_action('club')
            
            if player.animation_frame >= len(e.animation_higher_database['player']['club'][0]) - 1:
                is_wielding_club = False
                club.clear()
                player.set_action('idle')
                
                
                    
        elif is_shooting_arrow:
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


        pygame.mixer.music.stop()
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
                # if event.key == K_w:
                #     pygame.mixer.music.fadeout(1000)
                if event.key == K_RIGHT:
                    moving_right = True
                if event.key == K_LEFT:
                    moving_left = True
                if event.key == K_UP:
                    if air_timer < 6:
                        jump_sound.play()
                        vertical_momentum = -5
                if event.key == K_a and not is_wielding_club:
                    is_wielding_club = True
                    club.append([e.entity(player.x + 12, player.y-13, 22, 29, 'club')])
                        
                       
                    
                elif event.key == K_s and arrow_cnt:
                    is_shooting_arrow = True
                    arrow_shoot_sound.play()

                    if player.flip == False: arrow_objects.append([player.flip , e.entity(player.x + 13, player.y + 12, 13, 1, 'arrow')])
                    else: arrow_objects.append([player.flip , e.entity(player.x - 13, player.y + 12, 13, 1, 'arrow')])
                    arrow_cnt -= 1
                    
            if game_over == True:
                
                
                if event.key == K_r:
                    game_over = False
                    
                    score = 0
                    current_health = 200
                    player = e.entity(100,0,10,26,'player')
                    enemies.clear()
                    arrow_objects.clear()
                    meats.clear()
                    pygame.mixer.music.play()
                    game_time = 0
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
    day_board = game_font.render('days : ' + str(days), True, (255, 255, 255))
    #arrow_board = game_font.render('arrow : ' + str(arrow_cnt), True, (255, 255, 255))
    
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0, 10))
    screen.blit(score_board, (20, 50))
    screen.blit(day_board, (1050, 20))
    #screen.blit(arrow_board, (10, 90))

    for i in range(1, arrow_cnt+1):
        screen.blit(arrow_cnt_img, (20*i, 90))

    
    pygame.display.update()
