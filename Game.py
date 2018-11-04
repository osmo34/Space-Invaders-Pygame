# space invaders clone 2018 - Steve O https://github.com/osmo34
# CS50 final project

import pygame
import random

# init pygame
pygame.init()
screen = pygame.display.set_mode((1024, 768))
done = False # game loop

clock = pygame.time.Clock()

# load sprites - current images being used are from Kenny https://www.kenney.nl/assets/space-shooter-redux
player_sprite = pygame.image.load('playerShip2_green.png') 
player_projectile_sprite = pygame.image.load('laserBlue07.png') 
enemy_projectile_sprite = pygame.image.load('laserRed03.png') 
enemy_sprite = pygame.image.load('enemyBlue2.png')
explosion_sprite = [pygame.image.load('explosion1.png'), pygame.image.load('explosion2.png'), pygame.image.load('explosion3.png'), pygame.image.load('explosion4.png'), pygame.image.load('explosion5.png'), pygame.image.load('explosion6.png'), pygame.image.load('explosion7.png'), pygame.image.load('explosion8.png')]

# background
background_sprite = pygame.image.load('background_01.png').convert()

# scale sprites
player_sprite = pygame.transform.scale(player_sprite, (28, 19))
player_projectile_sprite = pygame.transform.scale(player_projectile_sprite, (5, 25))
enemy_projectile_sprite = pygame.transform.scale(enemy_projectile_sprite, (5, 25))
enemy_sprite = pygame.transform.scale(enemy_sprite, (26, 21))
for i in range(len(explosion_sprite)):
    explosion_sprite[i] = pygame.transform.scale(explosion_sprite[i], (64, 64))

# music
game_music_1 = pygame.mixer.music.load('Steamtech-Mayhem.ogg')

# sound effects
player_laser = pygame.mixer.Sound('sound_spark_Laser-Like_Synth_Basic_Laser1_14.wav')
enemy_exploision = pygame.mixer.Sound('Explosion+3.wav')
enemy_exploision.set_volume(0.05)
player_laser.set_volume(0.1)

# player globals
player_start_x = 500
player_start_y = 700

player_projectile_speed = 10

# ememy globals
enemy_speed = 2
enemy_speed_left = -2
enemy_speed_right = 2
enemy_drop_height = 2 # how many pixels we should move down on hitting the edge of the screen
enemy_update_height = 0 # how many pixels we have moved down
enemy_horizontal_seperation = 50
enemy_vertical_seperation = 50
enemy_rows = 6
enemy_colums = 11
default_enemy_x_pos = 150
default_enemy_y_pos = 50
enemy_edge_right = 1000
enemy_edge_left = 0
enemy_fire_rate = 3000 # max seed

enemy_projectile_seed = -5


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
    def __init__(self, spr):
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

    def prepare(self, posx, posy):    
        offset = 16 # makes the explosion a bit higher
        self.pos_x = posx
        self.pos_y = posy - offset

    def update(self):

        if self.new_explosion:
            self.created_time = pygame.time.get_ticks()
            self.new_explosion = False

        self.seconds = (pygame.time.get_ticks() - self.created_time) / 500  # frame time half a second      

        if not self.stop:
            self.current_time += self.seconds
            if (self.current_image == 7):
                self.stop = True

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

    # player updates
    def update(self):        
        self.__updateInput()
        self.__updateProjectile()       
        self.__checkDead()
        
        
        
    # input updates
    def __updateInput(self):
        k_pressed = pygame.key.get_pressed()            
        if k_pressed[pygame.K_LEFT]: self.position_x -= self.speed
        if k_pressed[pygame.K_RIGHT]: self.position_x += self.speed
        
        if not self.projectile.firing:
            global player_laser
            if k_pressed[pygame.K_SPACE]:
                player_laser.play()
                self.projectile.firing = True

    def __updateProjectile(self):
        self.projectile.update(self.position_x + self.projectile_offset_x, self.position_y - self.projectile_offset_y)

    def __checkDead(self):
        if self.dead:
            self.position_x = 0 # todo: temp
            self.dead = False



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
    
    # define when an enemy fires
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
    
    # place enemies in the game window
    def initialize(self):
        for i in range(enemy_rows): 
            for z in range(enemy_colums): 
                self.enemy_list.append(Enemy(self.enemy_position_x, self.enemy_position_y))
                self.enemy_position_x += enemy_horizontal_seperation
            self.enemy_position_y += enemy_vertical_seperation
            self.enemy_position_x = default_enemy_x_pos
    
    # check if we hit an edge
    def update(self):
        self.enemy_movement.check_edge(self.enemy_list)
        for enemy in self.enemy_list:
            enemy.update()


    
    # draw all enemies
    def draw(self):
        for enemy in self.enemy_list:
            enemy.draw(enemy_sprite, enemy.position_x, enemy.position_y)
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
        self.explode = Explosion(explosion_sprite)

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

    def check_dead(self):
        if self.dead:            
            if not self.create_explosion:
                self.old_pos_x = self.position_x
                self.old_pos_y = self.position_y
                self.create_explosion = True
            # if dead throw position into no mans land - way off the screen
            self.position_x = -1000
            self.position_y = 1000

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


# create instances   
player = Player()
enemy_controller = EnemyController()
enemy_controller.initialize()
collision = Collision()
background = Sprite()

pygame.mixer.music.play(-1)

# run game loop
while not done:
    clock.tick(60) # tick at indicated fps

    # pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    # update game items
    player.update()
    enemy_controller.update()


    for enemies in enemy_controller.enemy_list:         
        if collision.checkCollision(enemies, player.projectile):
            enemy_exploision.play()
            enemies.dead = True
            player.projectile.hit_enemy = True
            break
        
    for enemies in enemy_controller.enemy_list:
        if collision.checkCollision(player, enemies.projectile):
            player.dead = True
            break
    

    # draw
    screen.fill((0,0,0))  
    background.draw(background_sprite, 0, 0)

    player.draw(player_sprite, player.position_x, player.position_y)
    if player.projectile.firing:
        player.projectile.draw(player_projectile_sprite, player.projectile.position_x, player.projectile.position_y)
    else:
        player.projectile.update_rect(player_projectile_sprite, player.projectile.position_x, player.projectile.position_y) # if we are not drawing we still need to track the sprite position
    enemy_controller.draw()


    pygame.display.update()


pygame.quit()

        

