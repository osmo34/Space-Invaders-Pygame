# space invaders clone 2018 - Steve O https://github.com/osmo34
# CS50 final project

import pygame

# init pygame
pygame.init()
screen = pygame.display.set_mode((1024, 768))
done = False # game loop

clock = pygame.time.Clock()

# load sprites - current images being used are from Kenny https://www.kenney.nl/assets/space-shooter-redux
player_sprite = pygame.image.load('playerShip2_green.png') 
enemy_sprite = pygame.image.load('enemyBlue2.png')

# scale sprites
player_sprite = pygame.transform.scale(player_sprite, (28, 19))
enemy_sprite = pygame.transform.scale(enemy_sprite, (26, 21))

# player globals
player_start_x = 500
player_start_y = 700

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


# sprite base class
class Sprite:
    # draw which should be inherited
    def draw(self, sprite, pos_x, pos_y):
        screen.blit(sprite, (pos_x, pos_y))
        


# player class
class Player(Sprite): 
    def __init__(self):
        self.speed = 6
        self.position_x = player_start_x
        self.position_y = player_start_y

    # player updates
    def update(self):
        self.__updateInput()
        
    # input updates
    def __updateInput(self):
        k_pressed = pygame.key.get_pressed()            
        if k_pressed[pygame.K_LEFT]: self.position_x -= self.speed
        if k_pressed[pygame.K_RIGHT]: self.position_x += self.speed




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




# enemy class
class Enemy(Sprite):
    def __init__(self, pos_x, pos_y):
        self.position_x = pos_x
        self.position_y = pos_y
        self.initial_height = pos_y        

    def update(self):
        self.__move_enemy()
        self.__check_enemy_height()

    def __move_enemy(self):              
        self.position_x += enemy_speed        

    def __check_enemy_height(self):
        self.position_y = self.initial_height + enemy_update_height


# class for enemy movement
class EnemyMovement:
    def check_edge(self, enemies):        
        global enemy_speed
        global enemy_update_height

        for enemy in enemies:            
            if enemy.position_x >= enemy_edge_right:                
                enemy_speed = enemy_speed_left
                enemy_update_height += enemy_drop_height
            elif enemy.position_x <= enemy_edge_left:
                enemy_speed = enemy_speed_right
                enemy_update_height += enemy_drop_height



# create instances   
player = Player()
enemy_controller = EnemyController()
enemy_controller.initialize()

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
    
    # draw
    screen.fill((0,0,0))
    player.draw(player_sprite, player.position_x, player.position_y)
    enemy_controller.draw()
    pygame.display.update()


pygame.quit()

        

