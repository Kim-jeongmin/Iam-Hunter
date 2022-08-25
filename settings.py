import pygame

moving_right = False
moving_left = False
is_shooting_bullet = False
is_shooting_arrow = False
is_hitted = False
vertical_momentum = 0
air_timer = 0
game_over = False
game_over_timer = 0
score = 0
current_health  = 200
max_health = 200
hit_cooldown = 0
arrow_offence_power = 50

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
arrow_img = pygame.image.load('data/images/arrow.png')

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
meats = []





grass_sound_timer = 0