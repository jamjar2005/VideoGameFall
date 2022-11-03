# Sources: Mr. Cozort's Cource Code Files, Google search bar, W3 schools RGB calculator.
# content from kids can code: http://kidscancode.org/blog/
# import libraries and modules
# from platform import platform

'''
# Innovation...
# I added color toggle keys and 2 keys that make the acceleration super fast in either direction
# I added a roof by adding it to the Platforms class and allplats group
# I made the mobs move downwards by changing rect.x to rect.y and made them faster
# I changed the goal of the game to move laterally to avoid being hit by the mobs
# I changed the on-screen "score" to "hits" and made it subtract 1 every time mobhits = True
# Going to draw text on screen "YOU LOSE" if hits are equal to or less than 0
'''
# importing libraries
from ast import Delete
from textwrap import fill
from tkinter import RIGHT
from turtle import width
from typing import KeysView
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint

#defining the variable vec 
vec = pg.math.Vector2

# game settings 
WIDTH = 1400
HEIGHT = 900
FPS = 30

# player settings, also defining HITS at 20 which will be used to define loss conditions in the end.
PLAYER_GRAV = 7.5
PLAYER_FRIC = 0.1
HITS = 20

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 90, 0)

# Creates a list(array) of colors
colors = [WHITE, BLACK, RED, GREEN, BLUE, ORANGE]
# defining the draw_text function and parameters which will be used later to display hits and "YOU LOSE" message to the player. 
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

def colorbyte():
    return random.randint(0,255)

# This is the player class, where the player's attributes are defined. These include area, shape, color, etc.
# I modified self.pos to make the player spawn on the floor instead of in the air.
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.r = 0
        self.g = 0
        self.b = 255
        self.image.fill((self.r, self.g, self.b))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/1)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    
    # defining controls for the sprite "self" or in other words the player
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
            # Secret keys that cause super fast acceleration in either direction
        if keys[pg.K_j]:
            self.acc.x = -100
        if keys[pg.K_k]:
            self.acc.x = 100
        # Toggle keys for color
        if keys[pg.K_1]:
            self.image.fill(WHITE)
        if keys[pg.K_2]:
            self.image.fill(ORANGE)
        if keys[pg.K_3]:
            self.image.fill(RED)
        if keys[pg.K_4]:
            self.image.fill(GREEN)
        if keys[pg.K_5]:
            self.image.fill(BLUE)
        
    # defining jump for the class self.
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, all_plats, False)
        self.rect.x += -1
        if hits:
            self.vel.y = -27.5
    #defining update for the class self using PLAYER_GRAV. This also uses the previously defined player controls.
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # friction
        self.acc.x += self.vel.x * -0.1
        # self.acc.y += self.vel.y * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # self.rect.x += self.xvel
        # self.rect.y += self.yvel
        self.rect.midbottom = self.pos

# Creating a subclass for the platforms under the superclass of Sprite. Defining attributes for subclass.
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
# Creating another subclass for Mobs under the superclass Sprite. Same as other classes in terms of defining attributes.
class Mob(Sprite):
    def __init__(self, x, y, w, h, color):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.y += 5
        

# init pygame and create a window.
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()
  
# creating groups for the various classes
all_sprites = pg.sprite.Group()
all_plats = pg.sprite.Group()
mobs = pg.sprite.Group()

# instantiate classes
player = Player()
plat = Platform(180, 380, 100, 35)
plat2 = Platform(289, 180, 100, 35)
ground = Platform(0, HEIGHT-50, WIDTH, 400)
roof = Platform(0, HEIGHT -915, WIDTH, 50)

# Using a for loop to randomly spawn in the given value (150 in this case) of mobs within the given coordinates.
# Also, creating a variable "m" to house the class "Mob" to make it easier to add to the group all_sprites.
for i in range(150):
    m = Mob(randint(0,WIDTH), randint(0,HEIGHT+ 500), 25, 25, (colorbyte(),colorbyte(),colorbyte()))
    all_sprites.add(m)
    mobs.add(m)
    print(m)

# add player to all_sprites group.
# adding plat, plat2, ground, and roof to the all_plats group.
all_sprites.add(player)
all_plats.add(plat, plat2, ground, roof)

# add plat and plat2, ground and roof to all sprites group
all_sprites.add(plat)
all_sprites.add(plat2)
all_sprites.add(ground)
all_sprites.add(roof)

# Game loop
running = True
while running:
    # keep the loop running using clock followed by the FPS, which we defined as 30 in the first few lines.
    clock.tick(FPS)
    # defining hits and causing the player to rectify its position on top of the platform if it collides.
    hits = pg.sprite.spritecollide(player, all_plats, False)
    if hits:
        print("ive struck a plat")
        player.pos.y = hits[0].rect.top
        player.vel.y = 0
    # defining the variable "mobhits" and using an if statement to print the given message when "mobhits" (spritecollide = true)
    # subtracting 1 from the hits every time this is true.
    mobhits = pg.sprite.spritecollide(player, mobs, True)
    if mobhits:
        print("ive struck a mob")
        HITS +=-1
    # Using a for loop to check for a closed window
    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            # using an if statement to state that if spacebar is pressed, call the player.jump function.
            if event.key == pg.K_SPACE:
                player.jump()
        
    ############ Update ##############
    # update all sprites
    all_sprites.update()

    ############ Draw ################
    # using an if/else statement to flash the screen red if "mobhits" and otherwise, draw the background screen
    if mobhits:
        screen.fill(RED)
    else: 
        screen.fill(BLACK)


    # draw the number of hits, this is connected to HITS defined in the first few lines of the game.
    draw_text("HITS: " + str(HITS), 22, WHITE, WIDTH / 2, HEIGHT / 24)
    # Print loser message if HITS is less than or equal to the given value, which in this case is 10.
    if HITS <= 10:
        draw_text("YOU LOSE", 200, RED, WIDTH / 2, HEIGHT / 4)

    # draw the screen. this is very important as you would not be able to see anything otherwise.
    all_sprites.draw(screen)

    # buffer - after drawing everything, flip display
    pg.display.flip()

# quitting pygame
pg.quit()
