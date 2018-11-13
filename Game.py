# space invaders clone 2018 - Steve O https://github.com/osmo34
# CS50 final project

# polishing TODO:
# player death - goes off screen, slides back on
# on death player blows up - pause, score on screen - then game over screen
# score on game over screen

import pygame
import random
from enum import Enum, auto
import sqlite3

# database
high_scores = []
high_score = 0
db = sqlite3.connect('scores.db')
c = db.cursor()
c.execute('''CREATE TABLE if not exists score("INTEGER scores")''')
db.commit()

for row in c.execute('SELECT * FROM score'):
    high_scores.append(row)

def calculate_high_score():
    global high_score   
    
    if not high_scores:
        high_scores.append((0,))        
    
    get_score = max(high_scores)
    high_score = get_score[0]

calculate_high_score()

# init pygame
pygame.init()
screen = pygame.display.set_mode((1024, 768))
done = False # game loop

clock = pygame.time.Clock()

pygame.font.init()

# title screen
title_sprite = pygame.image.load('textures/title_screen/title.png') 
game_over_title_sprite = pygame.image.load('textures/title_screen/game_over.png')

# load sprites - current images being used are from Kenny https://www.kenney.nl/assets/space-shooter-redux
player_sprite = pygame.image.load('textures/player/playerShip2_green.png') 
player_projectile_sprite = pygame.image.load('textures/projectile/laserBlue07.png') 
enemy_projectile_sprite = pygame.image.load('textures/projectile/laserRed03.png') 

enemy_sprite = [
    pygame.image.load('textures/enemy/enemyBlack1.png'),
    pygame.image.load('textures/enemy/enemyBlack2.png'),
    pygame.image.load('textures/enemy/enemyBlack3.png'),
    pygame.image.load('textures/enemy/enemyBlack4.png'),
    pygame.image.load('textures/enemy/enemyBlack5.png'),
    pygame.image.load('textures/enemy/enemyBlue1.png'),
    pygame.image.load('textures/enemy/enemyBlue2.png'),
    pygame.image.load('textures/enemy/enemyBlue3.png'),
    pygame.image.load('textures/enemy/enemyBlue4.png'),
    pygame.image.load('textures/enemy/enemyBlue5.png'),
    pygame.image.load('textures/enemy/enemyGreen1.png'),
    pygame.image.load('textures/enemy/enemyGreen2.png'),
    pygame.image.load('textures/enemy/enemyGreen3.png'),
    pygame.image.load('textures/enemy/enemyGreen4.png'),
    pygame.image.load('textures/enemy/enemyGreen5.png'),
    pygame.image.load('textures/enemy/enemyRed1.png'),
    pygame.image.load('textures/enemy/enemyRed2.png'),
    pygame.image.load('textures/enemy/enemyRed3.png'),
    pygame.image.load('textures/enemy/enemyRed4.png'),
    pygame.image.load('textures/enemy/enemyRed5.png')
    ]

ufo_sprite = [
    pygame.image.load('textures/ufo/ufoBlue.png'),
    pygame.image.load('textures/ufo/ufoGreen.png'),
    pygame.image.load('textures/ufo/ufoRed.png'),
    pygame.image.load('textures/ufo/ufoYellow.png')
    ]

explosion_sprite = [
    pygame.image.load('textures/explosion_1/explosion1.png'), 
    pygame.image.load('textures/explosion_1/explosion2.png'), 
    pygame.image.load('textures/explosion_1/explosion3.png'), 
    pygame.image.load('textures/explosion_1/explosion4.png'), 
    pygame.image.load('textures/explosion_1/explosion5.png'), 
    pygame.image.load('textures/explosion_1/explosion6.png'), 
    pygame.image.load('textures/explosion_1/explosion7.png'), 
    pygame.image.load('textures/explosion_1/explosion8.png')
    ]

player_explosion_sprite = [
    pygame.image.load('textures/explosion_2/explosion1.png'), 
    pygame.image.load('textures/explosion_2/explosion2.png'), 
    pygame.image.load('textures/explosion_2/explosion3.png'), 
    pygame.image.load('textures/explosion_2/explosion4.png'), 
    pygame.image.load('textures/explosion_2/explosion5.png'), 
    pygame.image.load('textures/explosion_2/explosion6.png'), 
    pygame.image.load('textures/explosion_2/explosion7.png'), 
    pygame.image.load('textures/explosion_2/explosion8.png'),
    pygame.image.load('textures/explosion_2/explosion9.png'), 
    pygame.image.load('textures/explosion_2/explosion10.png'), 
    pygame.image.load('textures/explosion_2/explosion11.png'), 
    pygame.image.load('textures/explosion_2/explosion12.png'), 
    pygame.image.load('textures/explosion_2/explosion13.png'), 
    pygame.image.load('textures/explosion_2/explosion14.png'), 
    pygame.image.load('textures/explosion_2/explosion15.png'), 
    pygame.image.load('textures/explosion_2/explosion16.png'),
    pygame.image.load('textures/explosion_2/explosion17.png'), 
    pygame.image.load('textures/explosion_2/explosion18.png'), 
    pygame.image.load('textures/explosion_2/explosion19.png'), 
    pygame.image.load('textures/explosion_2/explosion20.png'), 
    pygame.image.load('textures/explosion_2/explosion21.png'), 
    pygame.image.load('textures/explosion_2/explosion22.png'), 
    pygame.image.load('textures/explosion_2/explosion23.png'), 
    pygame.image.load('textures/explosion_2/explosion24.png'),
    pygame.image.load('textures/explosion_2/explosion25.png'), 
    pygame.image.load('textures/explosion_2/explosion26.png'), 
    pygame.image.load('textures/explosion_2/explosion27.png'), 
    pygame.image.load('textures/explosion_2/explosion28.png')
    ]

# background
background_sprite = [
    pygame.image.load('textures/bg/background_01.png').convert(),
    pygame.image.load('textures/bg/background_02.png').convert(),
    pygame.image.load('textures/bg/background_03.png').convert()
    ]

background_current = 0

# scale sprites
player_sprite = pygame.transform.scale(player_sprite, (42, 28))
player_projectile_sprite = pygame.transform.scale(player_projectile_sprite, (5, 25))
enemy_projectile_sprite = pygame.transform.scale(enemy_projectile_sprite, (5, 25))

for i in range(len(enemy_sprite)):
    enemy_sprite[i] = pygame.transform.scale(enemy_sprite[i], (26, 21))

for i in range(len(ufo_sprite)):
    ufo_sprite[i] = pygame.transform.scale(ufo_sprite[i], (30, 30))

for i in range(len(explosion_sprite)):
    explosion_sprite[i] = pygame.transform.scale(explosion_sprite[i], (64, 64))

for i in range(len(player_explosion_sprite)):
    player_explosion_sprite[i] = pygame.transform.scale(player_explosion_sprite[i], (128, 128))

# music
game_music_1 = pygame.mixer.music.load('sound/Steamtech-Mayhem.ogg')

# sound effects
player_laser = pygame.mixer.Sound('sound/sound_spark_Laser-Like_Synth_Basic_Laser1_14.wav')
enemy_exploision = pygame.mixer.Sound('sound/Explosion+3.wav')
enemy_exploision.set_volume(0.05)
player_laser.set_volume(0.1)

# game globals
base_score = 0
base_lives = 3
score = base_score
lives = base_lives

# player globals
base_player_start_x = 500
base_player_start_y = 700
player_start_x = base_player_start_x
player_start_y = base_player_start_y
player_projectile_speed = 15

# ememy globals
base_enemy_speed = 2.0
base_enemy_speed_left = -2.0
base_enemy_speed_right = 2.0

enemy_speed = base_enemy_speed
enemy_speed_left = base_enemy_speed_left
enemy_speed_right = base_enemy_speed_right

enemy_speed_multiplier_base = 0.03
enemy_speed_last_5_base = 1.9
enemy_speed_multiplier_final_base = 10.0

enemy_speed_multiplier = enemy_speed_multiplier_base
enemy_speed_last_5 = enemy_speed_last_5_base
enemy_speed_multiplier_final = enemy_speed_multiplier_final_base

base_enemy_drop_height = 4 
base_enemy_drop_last_5 = 25
base_enemy_drop_last = 45
enemy_drop_height = base_enemy_drop_height # how many pixels we should move down on hitting the edge of the screen
enemy_drop_last_5 = base_enemy_drop_last_5
enemy_drop_last = base_enemy_drop_last

base_enemy_update_height = 0
enemy_update_height = base_enemy_update_height # how many pixels we have moved down
enemy_horizontal_seperation = 50
enemy_vertical_seperation = 50
enemy_rows = 6
enemy_colums = 11
default_enemy_x_pos = 150
default_enemy_y_pos = 50
enemy_edge_right = 1000
enemy_edge_left = 0
enemy_fire_rate_base = 1000
enemy_fire_rate = enemy_fire_rate_base # max seed
enemy_projectile_seed = -5
base_enemy_score = 50
enemy_score = base_enemy_score
enemy_count_base = enemy_rows * enemy_colums + 1
enemy_count = enemy_count_base
enemy_fire_rate_multiplier_base = enemy_fire_rate_base // enemy_count_base
enemy_fire_rate_multiplier = enemy_fire_rate_multiplier_base

level_current_base = 1
level_current = level_current_base

level_multiplier_base = 1
level_multiplier = level_multiplier_base

game_run_time = 0.0
final_time = 0.0

UFO_score_base = 1000
UFO_score = UFO_score_base
UFO_speed = 3.0

# game state
class GameState(Enum):
    TITLE_SCREEN = auto()
    IN_GAME = auto()
    GAME_OVER = auto()

game_state = GameState.TITLE_SCREEN

# classes #

# sprite base class
class Sprite:
    def __init__(self):
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0        

    # draw which should be inherited
    def draw(self, sprite, pos_x, pos_y):
        screen.blit(sprite, (pos_x, pos_y))
        self.update_rect(sprite, pos_x, pos_y)
        
    def update_rect(self, sprite, posx, posy):
        sprite_rect = sprite.get_rect()
        self.left = posx + sprite_rect.left
        self.right = posx + sprite_rect.right
        self.top = posy + sprite_rect.top
        self.bottom = posy + sprite_rect.bottom

        

# create explosion
class Explosion:
    def __init__(self, spr, offset):
        self.image_count = len(spr)
        self.sprite = spr        
        self.current_image = 0      
        self.seconds = 0.0
        self.current_time = self.seconds
        self.new_explosion = True
        self.created_time = 0
        self.stop = False
        self.pos_x = 0
        self.pos_y = 0
        self.reset = False
        self.offset = offset

    def prepare(self, posx, posy):    
        self.pos_x = posx - self.offset
        self.pos_y = posy - self.offset
        # reset counters for the player who could potentially blow up multiple times TODO: might be needed for enemies in multiple levels...
        if self.stop and self.reset:
            self.new_explosion = True
            self.stop = False
            self.reset = False

    def update(self):
        if self.new_explosion:
            self.created_time = pygame.time.get_ticks()
            self.new_explosion = False

        self.seconds = (pygame.time.get_ticks() - self.created_time) / 500  # frame time half a second      

        if not self.stop:
            self.current_time += self.seconds
            if (self.current_image == self.image_count - 1):                
                self.stop = True
                self.current_image = 0 

            if self.current_time >= 1:
                self.current_image += 1            
                self.current_time = 0

    def draw(self):
        if not self.stop:
            screen.blit(self.sprite[self.current_image], (self.pos_x, self.pos_y))



# player class
class Player(Sprite): 
    def __init__(self):
        super(Player, self).__init__()
        self.speed = 6
        self.position_x = player_start_x
        self.position_y = player_start_y
        self.projectile_offset_x = 11.5
        self.projectile_offset_y = 25
        self.projectile = Projectile(self.position_x + self.projectile_offset_x, self.position_y - self.projectile_offset_y, player_projectile_speed, False)
        self.dead = False
        self.hit_right = False
        self.hit_left = False
        self.create_explosion = False
        self.old_pos_x = 0
        self.old_pos_y = 0
        self.explode = Explosion(player_explosion_sprite, 64)

    # player updates
    def update(self):        
        self.__updateInput()
        self.__updateProjectile()       
        self.__checkDead()
        self.__checkEdge()
        self.explosion()           
        
    # input updates
    def __updateInput(self):
        k_pressed = pygame.key.get_pressed()
        if not self.hit_left:
            if k_pressed[pygame.K_LEFT]: self.position_x -= self.speed
        if not self.hit_right:
            if k_pressed[pygame.K_RIGHT]: self.position_x += self.speed
        
        if not self.projectile.firing:
            global player_laser
            if k_pressed[pygame.K_SPACE]:
                player_laser.play()
                self.projectile.firing = True

    def __updateProjectile(self):
        self.projectile.update(self.position_x + self.projectile_offset_x, self.position_y - self.projectile_offset_y)

    def __checkDead(self):
        global lives
        if self.dead:
            if not self.create_explosion: # get old positions for an explosion
                self.old_pos_x = self.position_x
                self.old_pos_y = self.position_y
                self.create_explosion = True
                lives -= 1
            self.position_x = 0 # todo: temp
            self.dead = False

    def __checkEdge(self):
        if self.position_x >= 950:
            self.hit_right = True
        elif self.position_x <= 50:
            self.hit_left = True
        else:
            self.hit_right = False
            self.hit_left = False

    def explosion(self):
        if self.create_explosion:            
            if not self.explode.stop or self.explode.reset:
                self.explode.prepare(self.old_pos_x, self.old_pos_y)
                self.explode.update()
            else:
                self.create_explosion = False
                self.explode.reset = True



# create projectiles
class Projectile(Sprite):
    def __init__(self, pos_x, pos_y, speed, enemy):
        super(Projectile, self).__init__()
        self.position_x = pos_x
        self.position_y = pos_y
        self.firing = False
        self.hit_enemy = False
        self.projectile_speed = speed
        self.is_enemy = enemy

    def update(self, pos_x, pos_y):                
        self.__move_projectile(pos_x, pos_y)
        if not self.is_enemy:            
            self.__check_screen_top(pos_x, pos_y)
            if self.hit_enemy:
                self.__hit_enemy(pos_x, pos_y)
        elif self.is_enemy:
            self.__check_screen_bottom(pos_x, pos_y)
            self.__enemy_fire()

    # check if projectile hit enemy - player only
    def __hit_enemy(self, pos_x, pos_y):        
        self.position_x = pos_x
        self.position_y = pos_y
        self.firing = False
        self.hit_enemy = False
    
    # move dependent on if we are firing or not
    def __move_projectile(self, pos_x, pos_y):
        if not self.firing:
            self.position_x = pos_x
            self.position_y = pos_y
        elif self.firing:
            self.position_y -= self.projectile_speed

    # only relevent for player projectile
    def __check_screen_top(self, pos_x, pos_y):
        if self.position_y <= 0:
            self.position_x = pos_x
            self.position_y = pos_y
            self.firing = False

    # only relevent for enemy laser
    def __check_screen_bottom(self, pos_x, pos_y):
        if self.position_y >= 768:
            self.position_x = pos_x
            self.position_y = pos_y
            self.firing = False
    
    # define when an enemy fires TODO: change this - base on time, not a seed
    def __enemy_fire(self):
        # fire at random
        if not self.firing:
            seed = random.randint(1, enemy_fire_rate)
            if seed == 10: # doesn't matter what number this is, as long as it's under enemy_fire_rate 
                self.firing = True



# base controller for enemies
class EnemyController():
    def __init__(self):
        self.enemy_list = []
        self.enemy_movement = EnemyMovement()
        self.enemy_position_x = default_enemy_x_pos
        self.enemy_position_y = default_enemy_y_pos
        self.game_over = False
        self.hit_bottom = False
    
    # place enemies in the game window
    def initialize(self):
        for i in range(enemy_rows): 
            for z in range(enemy_colums): 
                self.enemy_list.append(Enemy(self.enemy_position_x, self.enemy_position_y))
                self.enemy_position_x += enemy_horizontal_seperation
            self.enemy_position_y += enemy_vertical_seperation
            self.enemy_position_x = default_enemy_x_pos

    def reset_enemies(self):
        if not self.game_over:
            self.enemy_list.clear()
            self.enemy_position_x = default_enemy_x_pos
            self.enemy_position_y = default_enemy_y_pos        
            self.initialize()
            self.game_over = True
            self.hit_bottom = False
    
    # check if we hit an edge
    def update(self):
        if not self.game_over:
            self.enemy_movement.check_edge(self.enemy_list)
            for enemy in self.enemy_list:
                enemy.update()
                if enemy.check_bottom_screen():
                    self.hit_bottom = True
    
    # draw all enemies
    def draw(self):
        for enemy in self.enemy_list:
            enemy.draw(enemy_sprite[enemy.sprite_type], enemy.position_x, enemy.position_y)
            if enemy.projectile.firing:                
                enemy.projectile.draw(enemy_projectile_sprite, enemy.projectile.position_x, enemy.projectile.position_y)                
            else:
                enemy.projectile.update_rect(enemy_projectile_sprite, enemy.projectile.position_x, enemy.projectile.position_y)

            if enemy.create_explosion:
                enemy.explode.draw()


# enemy class
class Enemy(Sprite):
    def __init__(self, pos_x, pos_y):
        super(Enemy, self).__init__()
        self.position_x = pos_x
        self.position_y = pos_y
        self.initial_height = pos_y
        self.projectile = Projectile(self.position_x + 11, self.position_y + 20, enemy_projectile_seed, True)
        self.dead = False
        self.create_explosion = False
        self.old_pos_x = 0
        self.old_pos_y = 0
        self.explode = Explosion(explosion_sprite, 16)

        # create sprite type at random
        self.sprite_type = random.randint(0, len(enemy_sprite) - 1)

    def update(self):
        self.__move_enemy()
        self.__check_enemy_height()
        self.projectile.update(self.position_x + 11, self.position_y + 20)
        self.check_dead()
        self.explosion()

    def __move_enemy(self):              
        self.position_x += enemy_speed        

    def __check_enemy_height(self):
        self.position_y = self.initial_height + enemy_update_height

    def _boost_speed(self):
        global enemy_speed
        if enemy_speed > 0:
            enemy_speed = enemy_speed_right
        elif enemy_speed < 0:
            enemy_speed = enemy_speed_left

    def check_dead(self):
        global score
        global enemy_fire_rate
        global enemy_speed
        global enemy_speed_left
        global enemy_speed_right
        global enemy_count
        global enemy_drop_height
        if self.dead:            
            if not self.create_explosion: # get old positions for an explosion
                self.old_pos_x = self.position_x
                self.old_pos_y = self.position_y
                self.create_explosion = True
                
                score += enemy_score
                enemy_fire_rate -= enemy_fire_rate_multiplier
                
                # make the game harder as we lose enemies
                if enemy_count > 6:                    
                    enemy_speed_left -= enemy_speed_multiplier
                    enemy_speed_right += enemy_speed_multiplier                    
                    self._boost_speed() # smooth speed up 

                elif enemy_count <= 6 and enemy_count > 2:                    
                    enemy_speed_left -= enemy_speed_last_5
                    enemy_speed_right += enemy_speed_last_5
                    enemy_drop_height = enemy_drop_last_5
                    self._boost_speed()

                elif enemy_count == 2:
                    enemy_speed_left_= -enemy_speed_multiplier_final
                    enemy_speed_right = enemy_speed_multiplier_final                             
                    enemy_drop_height = enemy_drop_last
                    self._boost_speed()

                enemy_count -= 1               

            # if dead throw position into no mans land - way off the screen
            self.position_x = -1000
            self.position_y = 1000

    # hit bottom of screen aka game over
    def check_bottom_screen(self):
        if self.position_y > 650 and not self.dead:
            return True
        else:
            return False

    def explosion(self):
        if self.create_explosion:
            self.explode.prepare(self.old_pos_x, self.old_pos_y)
            self.explode.update()



# class for enemy movement
class EnemyMovement:
    def check_edge(self, enemies):        
        global enemy_speed
        global enemy_update_height

        for enemy in enemies:
            if enemy.dead:
                enemy.position_x = enemy.position_x
                enemy.position_y = enemy.position_y
            elif enemy.position_x >= enemy_edge_right:                
                enemy_speed = enemy_speed_left
                enemy_update_height += enemy_drop_height
            elif enemy.position_x <= enemy_edge_left:
                enemy_speed = enemy_speed_right
                enemy_update_height += enemy_drop_height


# UFO
class UFO(Sprite):
    def __init__(self):
        self.current_sprite = 0
        self.start_pos_x = - 100
        self.pos_x = self.start_pos_x
        self.speed_x = UFO_speed
        self.pos_y = 35
        self.flying = False
        self.dead = False
        self.create_explosion = False
        self.old_pos_x = 0
        self.old_pos_y = 0
        self.explode = Explosion(explosion_sprite, 16)
        self.texture = 0

    def update(self):
        if self.flying:
            self.pos_x += self.speed_x
        if self.pos_x >= 1000:
            self.pos_x = self.start_pos_x
            self.flying = False       
        
        self.__start_flight()
        self.__checkDead()
        self.__get_textureID()
        self.explosion()    

    def __start_flight(self):
        if not self.flying:
            if game_run_time < 10:
                return
            else:
               seed = random.randint(1, 750)               
               if seed == 100:
                   self.flying = True

    def __checkDead(self):       
        if self.dead:
            if not self.create_explosion: # get old positions for an explosion
                self.old_pos_x = self.pos_x
                self.old_pos_y = self.pos_y
                self.create_explosion = True                           
            self.flying = False
            self.pos_x = self.start_pos_x
            self.dead = False
            global lives
            global score
            lives += 1
            score += UFO_score

    def __get_textureID(self):
        if not self.flying:
            seed = random.randint(0, 2)
            self.texture = seed            

    def explosion(self):
         if self.create_explosion:            
            if not self.explode.stop or self.explode.reset:
                self.explode.prepare(self.old_pos_x, self.old_pos_y)
                self.explode.update()
            else:
                self.create_explosion = False
                self.explode.reset = True


# all collisions
class Collision:
    def checkCollision(self, target, projectile):
        projectile_position = (projectile.left, projectile.right, projectile.top)
        target_position = (target.left, target.right, target.top, target.bottom)        
        
        # default position at start of game is 0 - ignore this
        if (projectile_position[0]) == 0:
            del projectile_position
            del target_position
            return False

        if projectile_position[0] <= target_position[1] and projectile_position[1] >= target_position[0] and projectile_position[2] <= target_position[3] and projectile_position[2] >= target_position[2]:                                                
            del projectile_position
            del target_position
            return True
        else:
            del projectile_position
            del target_position
            return False



# create on-screen text
class Hud:
    def __init__(self, text, font, colour, position):
        self.text = text
        self.font = font
        self.position = position
        self.colour = colour
        self.textsurface = self.font.render(self.text, False, self.colour)

    # call this when text needs to be updated
    def update(self, text):
        self.text = text
        self.textsurface = self.font.render(self.text, False, self.colour)

    def draw(self):
        screen.blit(self.textsurface, self.position)


# title screen
class TitleScreen(Sprite):
    def update(self):
        global game_state
        k_pressed = pygame.key.get_pressed()        
        if k_pressed[pygame.K_SPACE]:
            game_state = GameState.IN_GAME


# game over screen
class GameOverScreen(Sprite):
    def __ini__(self):
        self.score = 0

    def get_score_value(self, score):
        self.score = score

    def update(self):
        global game_state
        k_pressed = pygame.key.get_pressed()        
        if k_pressed[pygame.K_RETURN]:            
            game_state = GameState.TITLE_SCREEN



# set up game
# create instances   
title_screen = TitleScreen()
game_over_screen = GameOverScreen()
player = Player()
enemy_controller = EnemyController()
enemy_controller.initialize()
collision = Collision()
background = Sprite()
ufo = UFO()

# create display text
font = pygame.font.Font('font/kenvector_future.ttf', 20)
green_text = (75, 244, 66)
yellow_text = (233, 244, 66)
hud_text = []
hud_text.append(Hud("Score", font, green_text, (10, 10)))
hud_text.append(Hud("Lives", font, green_text, (400, 10)))
hud_text.append(Hud("High Score", font, green_text, (700, 10)))

# text that needs to be updated at runtime
info_text = []
show_high_score = int(high_score)
text_display = [str(score), str(lives), str(show_high_score)]
info_text.append(Hud(text_display[0], font, yellow_text, (120, 10)))
info_text.append(Hud(text_display[1], font, yellow_text, (500, 10)))
info_text.append(Hud(text_display[2], font, yellow_text, (875, 10)))


# start music
pygame.mixer.music.play(-1)

def process_events():
    global done
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True    

# reset game
def reset_game():    
    global lives
    global score
    global player_start_x
    global player_start_y
    global enemy_speed
    global enemy_speed_left
    global enemy_speed_right
    global enemy_drop_height
    global enemy_drop_last_5
    global enemy_drop_last
    global enemy_update_height
    global enemy_score
    global enemy_count
    global enemy_fire_rate_multiplier
    global enemy_fire_rate
    global level_current
    global level_multiplier
    global player
    global game_run_time
    global final_time
    global enemy_speed_multiplier
    global enemy_speed_last_5
    global enemy_speed_multiplier_final    

        
    player_start_x = base_player_start_x    
    player.position_x = player_start_x    
    enemy_speed = base_enemy_speed
    enemy_speed_left = base_enemy_speed_left
    enemy_speed_right = base_enemy_speed_right
    enemy_drop_height = base_enemy_drop_height
    enemy_drop_last_5 = base_enemy_drop_last_5
    enemy_drop_last = base_enemy_drop_last
    enemy_update_height = base_enemy_update_height
    enemy_score = base_enemy_score
    enemy_count = enemy_count_base
    enemy_fire_rate = enemy_fire_rate_base
    enemy_fire_rate_multiplier = enemy_fire_rate_multiplier_base
    enemy_speed_multiplier = enemy_speed_multiplier_base
    enemy_speed_last_5 = enemy_speed_last_5_base
    enemy_speed_multiplier_final = enemy_speed_multiplier_final_base
    level_current = level_current_base
    level_multiplier = level_multiplier_base
    player.dead = False
    enemy_controller.reset_enemies()
    final_time += game_run_time
    game_run_time = 0

def death_reset():
    global score
    global lives
    global background_current
    score = base_score
    lives = base_lives
    background_current = 0

# todo - increase level
def increase_level():
    reset_game()   

    global enemy_speed
    global enemy_speed_left
    global enemy_speed_right
    global enemy_speed_multiplier
    global enemy_speed_last_5
    global enemy_speed_multiplier_final
    global enemy_drop_height
    global enemy_drop_last_5
    global enemy_drop_last
    global enemy_score
    global background_current

    # make it harder
    enemy_speed += 0.1
    enemy_speed_left -= 0.1
    enemy_speed_right += 0.1
    enemy_speed_multiplier += 0.02
    enemy_speed_last_5 += 0.2
    enemy_speed_multiplier_final += 3
    enemy_drop_height += 1
    enemy_drop_last_5 += 5
    enemy_drop_last += 5
    enemy_score *= 2

    # change backdrop
    if background_current == 2:
        background_current = 0
    else:
        background_current += 1


# run game loop
while not done:
    while game_state == GameState.TITLE_SCREEN and not done:
        process_events()
        title_screen.update()        
        screen.fill((0,0,0))  
        title_screen.draw(title_sprite, 0, 0)
        pygame.display.update()
    
    while game_state == GameState.GAME_OVER and not done:
        process_events()
        game_over_screen.update()
        screen.fill((0,0,0))  
        title_screen.draw(game_over_title_sprite, 0, 0)
        pygame.display.update()
    
    while game_state == GameState.IN_GAME and not done:        
        clock.tick(60) # tick at indicated fps

        # timer variable 
        game_run_time = pygame.time.get_ticks() / 1000 - final_time               

        # we hit a new game and ensure we are not in game over state
        if enemy_controller.game_over:
            enemy_controller.game_over = False

        # pygame events
        process_events()       

        # update game items
        player.update()
        enemy_controller.update()

         # ufo        
        ufo.update()   

        # track score per enemy
        enemy_score = base_enemy_score * abs(enemy_speed) * level_multiplier

        # update lives and score text
        for i in range(len(info_text)):
            text_display.clear()
            _show_score = int(high_score)
            text_display = [str(int(score)), str(lives), str(_show_score)]
            info_text[i].update(text_display[i])

        # check collisions
        for enemies in enemy_controller.enemy_list:         
            if collision.checkCollision(enemies, player.projectile):
                enemy_exploision.play()
                enemies.dead = True
                player.projectile.hit_enemy = True
                break
            if collision.checkCollision(player, enemies.projectile):
                player.dead = True
                break
        
        # end game
        if lives == 0 or enemy_controller.hit_bottom: # TODO - or enemy hits bottom of screen 
            # update scores, update high score if we have the highest value            
            score = abs(score)
            c.execute("INSERT INTO score VALUES (?)", (score,)) 
            db.commit()
            high_scores.append((score,))
            calculate_high_score()
            # start reset
            reset_game()
            death_reset()
            game_over_screen.get_score_value(score)
            game_state = GameState.GAME_OVER
            
        # Complete level
        if enemy_count == 1:
            increase_level()    
        
        # draw
        screen.fill((0,0,0))  
        background.draw(background_sprite[background_current], 0, 0)

        player.draw(player_sprite, player.position_x, player.position_y)
        if player.projectile.firing:
            player.projectile.draw(player_projectile_sprite, player.projectile.position_x, player.projectile.position_y)
        else:
            player.projectile.update_rect(player_projectile_sprite, player.projectile.position_x, player.projectile.position_y) # if we are not drawing we still need to track the sprite position
        if player.create_explosion:
            player.explode.draw()
        enemy_controller.draw()

        ufo.draw(ufo_sprite[ufo.texture], ufo.pos_x, ufo.pos_y)
        if ufo.create_explosion:
            ufo.explode.draw()
        # fussy - only works after draw code - ufo collisions
        if collision.checkCollision(ufo, player.projectile):
            ufo.dead = True
            break

        # draw hud items
        for text in hud_text:
            text.draw()

        for text in info_text:
            text.draw()
    
        pygame.display.update()

db.close()
pygame.quit()

        

