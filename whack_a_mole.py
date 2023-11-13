import pygame
import os
import random

from os import path
from pygame.locals import *

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

WIDTH = 800
HEIGHT = 600
FPS = 60

# RGB
WHITE = (255, 255, 255)
BALCK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BG = (17, 166, 41)

COL = 3
ROW = 3

def random_mole_position():
    random_land = random.choice(land_list_rect)
    mole_rect.midbottom = random_land.midtop

def draw_land():
    x , y = 0 , 0
    for row in range(ROW):
        x = 0
        for col in range(COL):
            screen.blit(land, (x * 200 + 140, y * 200 + 100))
            rect = pygame.Rect(x * 200 + 140, y * 200 + 190, 100, 50)
            # pygame.draw.rect(screen, BLUE, (rect))
            land_list_rect.append(rect)
            x += 1
        y += 1

def draw_text(text, font_size, font_color, x, y):
    font = pygame.font.SysFont(None, font_size)
    font_surface = font.render(text, True, font_color)
    screen.blit(font_surface, (x, y))

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack-a-Mole")
clock = pygame.time.Clock()

# game variable
mouse_pos = (0, 0)
pygame.mouse.set_visible(False)
countdown = 5
last_update = pygame.time.get_ticks()

# load sound
bonk = pygame.mixer.Sound(path.join(img_folder, 'bonk.mp3'))

# load images
mole = pygame.transform.scale(pygame.image.load(path.join(img_folder, 'mice.png')), (70, 70))
mole_rect = mole.get_rect()

land = pygame.transform.scale(pygame.image.load(path.join(img_folder, 'land.png')).convert_alpha(), (100, 90))
land_list_rect = []

hammer = []
for i in range(1, 3):
    img = pygame.image.load(path.join(img_folder, 'hammer{}.png'.format(i))).convert_alpha
    hammer.append(img)

hammer_img = hammer[0]
hammer_surface = pygame.transform.scale(hammer_img(), (200, 200))
hammer_rect = hammer_surface.get_rect()

run = True
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if mole_rect.collidepoint(mouse_pos):
                    bonk.play()
                hammer_img = hammer[1]
                hammer_surface = pygame.transform.scale(hammer_img(), (200, 200))
                random_mole_position()
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                hammer_img = hammer[0]
                hammer_surface = pygame.transform.scale(hammer_img(), (200, 200)) 

        mouse_pos = pygame.mouse.get_pos()
        hammer_rect.center = (mouse_pos[0], mouse_pos[1])

    pygame.display.flip()

    now = pygame.time.get_ticks()
    if now - last_update > 1000 and countdown > 0:
        last_update = now
        countdown -= 1
        random_mole_position()

    screen.fill(BG)
    if countdown > 0:
        draw_text(str(countdown), 40, WHITE, WIDTH//2, 20)
    else:
        screen.blit(mole, mole_rect)
    draw_land()
    screen.blit(hammer_surface, hammer_rect)

pygame.quit()