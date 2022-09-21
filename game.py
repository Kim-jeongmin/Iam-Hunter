import pygame, sys, random, noise
import data.engine as e
import main_menu as mm
from settings import *
clock = pygame.time.Clock()

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() # initiates pygame
pygame.mixer.set_num_channels(64)

pygame.display.set_caption('I\'m Hunter')
WINDOW_SIZE = (1200,800)
my_big_font = e.Font('data/font/large_font.png')
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
wielding_sound = pygame.mixer.Sound('data/audio/wield.wav')
jump_sound = pygame.mixer.Sound('data/audio/jump.wav')
grass_sounds = [pygame.mixer.Sound('data/audio/grass_0.wav'),pygame.mixer.Sound('data/audio/grass_1.wav')]
arrow_shoot_sound.set_volume(0.2)
hit_sound.set_volume(0.2)
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)
wielding_sound.set_volume(0.4)





player = e.entity(0,0,10,26,'player')


airplane=0
club=0


#for i in range(5):
#    spike_objects.append(e.spike((random.randint(0, 600)-300, 147)))

#for i in range(5):
#    jump_pole_objects.append(e.jump_pole((random.randint(0, 600)-300, 90)))


for i in range(2):
    enemies.append([0, e.entity(random.randint(player.x - 500, player.x - 400), random.randint(-100, -50), 15, 16, 'bunny'), 50])
    enemies.append([0, e.entity(random.randint(player.x + 400, player.x + 500), random.randint(-100, -50) , 15, 20, 'monkey'), 100])
  
mm.show_start_screen()




while True: # game loop
    clock.tick(60)
    if game_time == 0: airplane = e.entity(player.x+400, player.y-150, 16, 12, 'airplane')
    if game_time <= 1200 : 
        display.fill((146,244,255)) # clear screen by filling it with blue
        is_night = False
    elif 1200 < game_time <= 1300: display.fill((243,138,110)) 
    elif 1300 < game_time <= 1400: display.fill((201,109,127))
    elif 1400 < game_time <= 1500: 
        display.fill((125,94,128))
    elif 1500 < game_time <= 1600: display.fill((87,68,111))
    else: 
        if game_time == 1601: 
            for i in range(5):
                enemies.append([0, e.entity(random.randint(player.x - 500, player.x - 400), random.randint(-100, -50), 15, 16, 'bunny'), 50])
                enemies.append([0, e.entity(random.randint(player.x + 400, player.x + 500), random.randint(-100, -50) , 15, 20, 'monkey'), 100])
        display.fill((19,26,98))
        is_night = True
    
    if game_time == 1400: pygame.mixer.music.fadeout(1000)

    if game_time == 1500: 
        pygame.mixer.music.load('data/audio/night.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    if game_time == 0:
        pygame.mixer.music.load('data/audio/noon.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
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
        for i in range(3+days):
            enemies.append([0, e.entity(random.randint(player.x - 500, player.x - 400), random.randint(-100, -50), 15, 16, 'bunny'), 50])
            enemies.append([0, e.entity(random.randint(player.x + 400, player.x + 500), random.randint(-100, -50), 15, 20, 'monkey'), 100])

    # 적 
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
                enemy_movement[0] = 1.5
                enemy[1].set_flip(True)
            if player.x < enemy[1].x - 5:
                enemy_movement[0] = -1.5
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
                if enemy[1].type == 'bunny' : current_health -= 10 + days * 2
                elif enemy[1].type == 'monkey' : current_health -= 20 + days * 3
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

                r = random.randint(1, 15)
                if r == 1 : items.append([e.entity(enemy[1].x, enemy[1].y + 5, 16, 16, 'meat')])
                
                if random.randint(0, 5) == 0:
                    meats.append([-2, e.entity(enemy[1].x, enemy[1].y, 16, 16, 'meat'), 0])
        
        if enemy[1].action == 'hit':
            if enemy[1].animation_frame >= len(e.animation_higher_database['monkey']['hit'][0]) - 1:
                enemy[1].set_action('idle')

        
        # hp bar
        pygame.draw.rect(display, RED, (enemy[1].x - scroll[0] - 5, enemy[1].y - scroll[1] - 10, 20, 2))
        pygame.draw.rect(display, GREEN, (enemy[1].x - scroll[0] - 5, enemy[1].y - scroll[1] - 10, enemy[2]/ 5, 2))
        enemy[1].change_frame(1)
        enemy[1].display(display, scroll)
    


    # 방망이
    
    if club != 0:    
        if player.flip == True:
            club.x = player.x - 12
            club.y = player.y - 10
            club.obj.rect.x = player.x - 12
            club.obj.rect.y = player.y - 10
            club.set_flip(True)
        elif player.flip == False:
            club.x = player.x 
            club.y = player.y - 10
            club.obj.rect.x = player.x
            club.obj.rect.y = player.y - 10
            club.set_flip(False)

        for enemy in enemies:
            if not enemy[1].action == 'die' and enemy[1].obj.rect.colliderect(club.obj.rect):
                if enemy[1].action == 'idle' or enemy[1].action == 'rage':
                    enemy[2] -= 30
                if enemy[2] > 0: 
                    enemy[1].set_action('hit')
                    enemy[0] = -2

                if player.flip == False:
                    enemy[1].x += 5
                else :
                    enemy[1].x -= 5

        club.change_frame(1)
        club.display(display, scroll)

    # 화살
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

    # 아이템        
    for item in items:        
        item_movement = [0,3]
        
        item[0].move(item_movement, tile_rects)

        if player.obj.rect.colliderect(item[0].obj.rect):
            if item[0].type == 'arrow_item' :  arrow_cnt += 5
            if item[0].type == 'meat' : current_health += 30
            if item[0].type == 'volt_item' : volt_cnt += 1
            if item[0].type == 'nut_item' : nut_cnt += 1
            if item[0].type == 'steel_item' : steel_cnt += 1
            
            items.remove(item)

            

        item[0].change_frame(1)
        item[0].display(display, scroll)

        
    # 비행기
    airplane_movement = [-2,0]
    collision_types = airplane.move(airplane_movement, tile_rects)

    airplane.change_frame(1)
    airplane.display(display, scroll)

    if  player.x - 1 <= airplane.x and airplane.x <= player.x + 1:
        r = random.randint(1, 5)
        
        if r == 2 : items.append([e.entity(airplane.x, airplane.y + 5, 16, 16, 'arrow_item')])
        elif r == 3 : items.append([e.entity(airplane.x, airplane.y + 5, 9, 9, 'volt_item')])
        elif r == 4 : items.append([e.entity(airplane.x, airplane.y + 5, 12, 10, 'nut_item')])
        elif r == 5 : items.append([e.entity(airplane.x, airplane.y + 5, 14, 12, 'steel_item')])
        
        
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
        else :
            if is_hitted:
                player.set_action('hit')
                if player.animation_frame >= len(e.animation_higher_database['player']['hit'][0]) - 1:
                    is_hitted = False     
            else :                                             
                if is_wielding_club:
                    player.set_action('club')
                    
                    if player.animation_frame >= len(e.animation_higher_database['player']['club'][0]) - 1:
                        is_wielding_club = False
                        club = 0
                        player.set_action('idle')
                if is_shooting_arrow:
                    player.set_action('arrow')
                    if player.animation_frame >= len(e.animation_higher_database['player']['arrow'][0]) - 1:
                        is_shooting_arrow = False
            
            
            

    if game_over:
        moving_right = False
        moving_left = False
        
        player.set_action('die')

        club = 0
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
                        vertical_momentum = -3
                if event.key == K_a and not is_wielding_club:
                    is_wielding_club = True
                    club = e.entity(player.x + 12, player.y-13, 22, 29, 'club')
                    wielding_sound.play()
                       
                    
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
                    player = e.entity(player.x,player.y - 100,10,26,'player')
                    enemies.clear()
                    arrow_objects.clear()
                    meats.clear()
                    pygame.mixer.music.play()
                    days = 0
                    arrow_cnt = 10
                    game_time = 0
                    
                    volt_cnt = 0
                    nut_cnt = 0
                    steel_cnt = 0
                    for i in range(3):
                        enemies.append([0, e.entity(random.randint(player.x - 500, player.x - 400), random.randint(-100, -50), 15, 16, 'bunny'), 50])
                        enemies.append([0, e.entity(random.randint(player.x + 400, player.x + 500), random.randint(-100, -50), 15, 20, 'monkey'), 100])

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
    
    

    # hp bar
    pygame.draw.rect(display, RED, (45, 23, max_health, 5))
    pygame.draw.rect(display, GREEN, (45, 23, current_health, 5))
    

    
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0, 0))
    #score_board = my_big_font.render(screen, 'score : ' + str(score), (600, 15))
    day_board = my_big_font.render(screen, 'days : ' + str(days) , (1050, 15) )

    screen.blit(volt_img, (100, 20))
    if volt_cnt > 7 : volt_cnt = 10 
    volt_board = my_big_font.render(screen, '  : ' + str(volt_cnt) + '/' + str(7) , (100, 15))  
    

    screen.blit(nut_img, (230, 20))
    if nut_cnt > 7 : nut_cnt = 10
    nut_board = my_big_font.render(screen, '  : ' + str(nut_cnt) + '/' + str(7) , (230, 15))  


    screen.blit(steel_img, (360, 20))
    if steel_cnt > 7 : steel_cnt = 10
    steel_board = my_big_font.render(screen, '  : ' + str(steel_cnt) + '/' + str(10) , (360, 15)) 

    if volt_cnt == 7 and nut_cnt == 7 and steel_cnt == 10:
        game_clear = True

    # player condition
    if current_health >= 100: screen.blit(player_conditions['healthy'][player_condition_count], (10, 10))
    elif 100 > current_health and current_health >= 40: screen.blit(player_conditions['hurt'][player_condition_count], (10, 10))
    elif 40 > current_health and current_health > 0: screen.blit(player_conditions['neardeath'][player_condition_count], (10, 10))
    else: screen.blit(player_conditions['death'][0], (10, 10))
    
    player_condition_count += 1
    if player_condition_count > 44:
        player_condition_count = 0

    for i in range(1, arrow_cnt+1):
        screen.blit(arrow_cnt_img, (20*i + 70, 70))

    
    pygame.display.update()
