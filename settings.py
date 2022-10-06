import pygame

moving_right = False
moving_left = False
is_wielding_club = False
is_shooting_arrow = False
is_hitted = False
vertical_momentum = 0
air_timer = 0
game_over = False
game_over_timer = 0
current_health  = 200
max_health = 200
hit_cooldown = 0
arrow_offence_power = 50
is_night = False
days = 0
arrow_cnt = 10
player_condition_count = 0
volt_cnt = 0
nut_cnt = 0
steel_cnt = 0
true_scroll = [0,0]

CHUNK_SIZE = 24

RED = (255, 0, 0)
GREEN = (0, 255, 0)

grass_img = pygame.image.load('data/images/grass.png').convert()
dirt_img = pygame.image.load('data/images/dirt.png').convert()
plant_img = pygame.image.load('data/images/plant.png').convert()
spike_img = pygame.image.load('data/images/spike.png').convert()
jump_pole_img = pygame.image.load('data/images/jump_pole.png').convert()
bullet_img = pygame.image.load('data/images/bullet.png').convert()
game_over_img = pygame.image.load('data/images/game_over.png')
tree_img = pygame.image.load('data/images/tree.png')
stone_img = pygame.image.load('data/images/stone.png')
cloud_img = pygame.image.load('data/images/cloud.png')
arrow_cnt_img = pygame.image.load('data/images/arrow_count.png')
volt_img = pygame.image.load('data/images/volt.png')
nut_img = pygame.image.load('data/images/nut.png')
steel_img = pygame.image.load('data/images/steel.png')

player_conditions = {}
player_conditions['healthy'] = {}
player_conditions['hurt'] = {}
player_conditions['neardeath'] = {}
player_conditions['death'] = {}

for i in range(0, 3):
    for j in range(0, 15):
        player_conditions['healthy'][j + i*15] = pygame.image.load('data/images/player_condition/healthy_' + str(i) + '.png')
        player_conditions['hurt'][j + i*15] = pygame.image.load('data/images/player_condition/hurt_' + str(i) + '.png')
        player_conditions['neardeath'][j + i*15] = pygame.image.load('data/images/player_condition/neardeath_' + str(i) + '.png')

player_conditions['death'][0] = pygame.image.load('data/images/player_condition/death_' + str(0) + '.png')

plant_img.set_colorkey((255,255,255))
spike_img.set_colorkey((0,0,0))
jump_pole_img.set_colorkey((0,0,0))

game_map = {}

tile_index = {
              1:grass_img,
              2:dirt_img,
              3:plant_img,
              4:tree_img,
              5:stone_img,
              6:cloud_img
              }

spike_objects = []
jump_pole_objects = []
bullet_objects = []
arrow_objects= []
enemies = []
items = []




game_time = 0

grass_sound_timer = 0