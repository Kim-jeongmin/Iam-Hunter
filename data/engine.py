import pygame, math, os
from pygame.locals import *

global e_colorkey
e_colorkey = (255,255,255)

def set_global_colorkey(colorkey):
    global e_colorkey
    e_colorkey = colorkey




# physics core

# 2d collisions test
def collision_test(object_1,object_list):
    collision_list = []
    for obj in object_list:
        if obj.colliderect(object_1):
            collision_list.append(obj)
    return collision_list

class map_obj():
    def __init__(self, loc):
        self.loc = loc
        
    def render(self, surf, scroll, img):
        surf.blit(img, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))
    
    

    def collision_test(self, rect):
        map_obj_rect = self.get_rect()
        return map_obj_rect.colliderect(rect)

# class spike(map_obj):
#     def __init__(self, loc):
#         super().__init__(loc)
        
#     def get_rect(self):
#         return pygame.Rect(self.loc[0], self.loc[1], 14, 13)

# class jump_pole(map_obj):
#     def __init__(self, loc):
#         super().__init__(loc)
        
#     def get_rect(self):
#         return pygame.Rect(self.loc[0], self.loc[1], 11, 16)


# class bullet(map_obj):
#     def __init__(self, loc, flip):
#         super().__init__(loc)
#         self.flip = flip

#     def get_rect(self):
#         return pygame.Rect(self.loc[0], self.loc[1], 1, 1)


    

# 2d physics object
class physics_obj(object):
   
    def __init__(self,x,y,x_size,y_size):
        self.width = x_size
        self.height = y_size
        self.rect = pygame.Rect(x,y,self.width,self.height)
        self.x = x
        self.y = y
       
    def move(self,movement,platforms,ramps=[]):
        self.x += movement[0]
        self.rect.x = int(self.x)
        block_hit_list = collision_test(self.rect,platforms)
        collision_types = {'top':False,'bottom':False,'right':False,'left':False,'slant_bottom':False,'data':[]}
        # added collision data to "collision_types". ignore the poorly chosen variable name
        for block in block_hit_list:
            markers = [False,False,False,False]
            if movement[0] > 0:
                self.rect.right = block.left
                collision_types['right'] = True
                markers[0] = True
            elif movement[0] < 0:
                self.rect.left = block.right
                collision_types['left'] = True
                markers[1] = True
            collision_types['data'].append([block,markers])
            self.x = self.rect.x
        self.y += movement[1]
        self.rect.y = int(self.y)
        block_hit_list = collision_test(self.rect,platforms)
        for block in block_hit_list:
            markers = [False,False,False,False]
            if movement[1] > 0:
                self.rect.bottom = block.top
                collision_types['bottom'] = True
                markers[2] = True
            elif movement[1] < 0:
                self.rect.top = block.bottom
                collision_types['top'] = True
                markers[3] = True
            collision_types['data'].append([block,markers])
            self.change_y = 0
            self.y = self.rect.y
        return collision_types


def flip(img,boolean=True):
    return pygame.transform.flip(img,boolean,False)
 
def blit_center(surf,surf2,pos):
    x = int(surf2.get_width()/2)
    y = int(surf2.get_height()/2)
    surf.blit(surf2,(pos[0]-x,pos[1]-y))
 
class entity(object):
    global animation_database, animation_higher_database
   
    def __init__(self,x,y,size_x,size_y,e_type): # x, y, size_x, size_y, type
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.obj = physics_obj(x,y,size_x,size_y)
        self.animation = None
        self.image = None
        self.animation_frame = 0
        self.animation_tags = []
        self.flip = False
        self.offset = [0,0]
        self.rotation = 0
        self.type = e_type # used to determine animation set among other things
        self.action_timer = 0
        self.action = ''
        self.set_action('idle') # overall action for the entity
        self.entity_data = {}
        self.alpha = None
 
    def set_pos(self,x,y):
        self.x = x
        self.y = y
        self.obj.x = x
        self.obj.y = y
        self.obj.rect.x = x
        self.obj.rect.y = y
 
    def move(self,momentum,platforms,ramps=[]):
        collisions = self.obj.move(momentum,platforms,ramps)
        self.x = self.obj.x
        self.y = self.obj.y
        return collisions
 
    def rect(self):
        return pygame.Rect(self.x,self.y,self.size_x,self.size_y)
 
    def set_flip(self,boolean):
        self.flip = boolean
 
    def set_animation_tags(self,tags):
        self.animation_tags = tags
 
    def set_animation(self,sequence):
        self.animation = sequence
        self.animation_frame = 0
 
    def set_action(self,action_id,force=False):
        if (self.action == action_id) and (force == False):
            pass
        else:
            self.action = action_id
            anim = animation_higher_database[self.type][action_id]
            self.animation = anim[0]
            self.set_animation_tags(anim[1])
            self.animation_frame = 0


    def get_center(self):
        x = self.x+int(self.size_x/2)
        y = self.y+int(self.size_y/2)
        return [x,y]
 
    def clear_animation(self):
        self.animation = None
 
    def set_image(self,image):
        self.image = image
 
    def set_offset(self,offset):
        self.offset = offset
 
    def set_frame(self,amount):
        self.animation_frame = amount
 
    def handle(self):
        self.action_timer += 1
        self.change_frame(1)
 
    def change_frame(self,amount):
        self.animation_frame += amount
        if self.animation != None:
            while self.animation_frame < 0:
                if 'loop' in self.animation_tags:
                    self.animation_frame += len(self.animation)
                else:
                    self.animation = 0
            while self.animation_frame >= len(self.animation):
                if 'loop' in self.animation_tags:
                    self.animation_frame -= len(self.animation)
                else:
                    self.animation_frame = len(self.animation)-1
                    
 

 
    def display(self,surface,scroll):
        image_to_render = None
        if self.animation == None:
            if self.image != None:
                image_to_render = flip(self.image,self.flip).copy()
        else:
            image_to_render = flip(animation_database[self.animation[self.animation_frame]],self.flip).copy()
        if image_to_render != None:
            center_x = image_to_render.get_width()/2
            center_y = image_to_render.get_height()/2
            image_to_render = pygame.transform.rotate(image_to_render,self.rotation)
            if self.alpha != None:
                image_to_render.set_alpha(self.alpha)
            blit_center(surface,image_to_render,(int(self.x)-scroll[0]+self.offset[0]+center_x,int(self.y)-scroll[1]+self.offset[1]+center_y))
 
# animation stuff

# global animation_database
animation_database = {}
 
# global animation_higher_database
animation_higher_database = {}
 
# a sequence looks like [[0,1],[1,1],[2,1],[3,1],[4,2]]
# the first numbers are the image name(as integer), while the second number shows the duration of it in the sequence
def animation_sequence(sequence,base_path,colorkey=(0, 0, 0),transparency=255):
    global animation_database
    result = []
    for frame in sequence:
        image_id = base_path + base_path.split('/')[-2] + '_' + str(frame[0])
        image = pygame.image.load(image_id + '.png').convert()
        image.set_colorkey(colorkey)
        image.set_alpha(transparency)
        animation_database[image_id] = image.copy()
        for i in range(frame[1]):
            result.append(image_id)
    return result
 
 
def get_frame(ID):
    global animation_database
    return animation_database[ID]
 
def load_animations(path):
    global animation_higher_database, e_colorkey
    f = open(path + 'entity_animations.txt','r')
    data = f.read()
    f.close()
    for animation in data.split('\n'):
        sections = animation.split(' ')
        anim_path = sections[0]
        entity_info = anim_path.split('/')
        entity_type = entity_info[0]
        animation_id = entity_info[1]
        timings = sections[1].split(';')
        tags = sections[2].split(';')
        sequence = []
        n = 0
        for timing in timings:
            sequence.append([n,int(timing)])
            n += 1
        anim = animation_sequence(sequence,path + anim_path,e_colorkey)
        if entity_type not in animation_higher_database:
            animation_higher_database[entity_type] = {}
        animation_higher_database[entity_type][animation_id] = [anim.copy(),tags]


def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

class Font():
    def __init__(self, path):
        self.spacing = 1
        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
        font_img = pygame.image.load(path)
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['A'].get_width()

    def render(self, surf, text, loc):
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing