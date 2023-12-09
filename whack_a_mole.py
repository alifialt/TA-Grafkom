import pygame, sys
from button import Button
import os
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from os import path
from pygame.locals import *

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
audio_folder = os.path.join(game_folder, 'audio')

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL | OPENGLBLIT)
pygame.display.set_caption('Menu')

glutInit()

gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

BG = pygame.image.load(path.join(img_folder, 'land.png'))

def get_font(size):
    return pygame.font.Font(path.join(img_folder, 'Roboto-Regular.ttf'))

def play():
    pygame.display.set_caption("Play")

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        WIDTH = 800
        HEIGHT = 600
        FPS = 60

        # RGB
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        GREEN = (0, 255, 0)
        BG = (17, 166, 41)

        COL = 3
        ROW = 3

        def random_mole_position():
            random_land = random.choice(land_list_rect)
            mole_rect.midbottom = random_land.midtop
            return random_land[1] - 70

        def draw_land():
            x , y = 0 , 0
            for row in range(ROW):
                x = 0
                for col in range(COL):
                    screen.blit(land, (x * 200 + 140, y * 200 + 100))
                    rect = pygame.Rect(x * 200 + 140, y * 200 + 190, 100, 50)
                    land_list_rect.append(rect)
                    x += 1
                y += 1

        def draw_text(text, font_size, font_color, x, y):
            font = pygame.font.SysFont(None, font_size)
            font_surface = font.render(text, True, font_color)
            screen.blit(font_surface, (x, y))

        def set_level_speed(level):
            speeds = [3000, 2000, 3000]
            return speeds[level - 1] if 0 <= level - 1 < len(speeds) else speeds[0]

        pygame.init()
        pygame.mixer.init()

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Whack-a-Mole")
        clock = pygame.time.Clock()

        # game variable
        mouse_pos = (0, 0)
        pygame.mouse.set_visible(False)
        countdown = 5
        level_durations = [6000, 5000, 4000]
        current_level = 1
        last_update = pygame.time.get_ticks()
        score = 0
        last_mole_move = pygame.time.get_ticks()
        current_sc = 0
        pos = 0
        game_start_time = 0
        game_over_time = 0
        
        # load sound
        bonk = pygame.mixer.Sound(path.join(audio_folder, 'bonk.mp3'))

        # load images
        mole = pygame.transform.scale(pygame.image.load(path.join(img_folder, 'mice.png')), (70, 70))
        mole_rect = mole.get_rect()

        land = pygame.transform.scale(pygame.image.load(path.join(img_folder, 'land.png')).convert_alpha(), (100, 90))
        land_list_rect = []

        hammer = []
        for i in range(1, 3):
            img = pygame.image.load(path.join(img_folder, 'hammer{}.png'.format(i))).convert_alpha()
            hammer.append(img)

        hammer_img = hammer[0]
        hammer_surface = pygame.transform.scale(hammer_img, (200, 200))
        hammer_rect = hammer_surface.get_rect()
        draw_land()

        exit_button = pygame.transform.scale(pygame.image.load(path.join(img_folder, 'exit_button.png')).convert_alpha(), (100, 50))
        exit_button_rect = exit_button.get_rect()
        exit_button_rect.center = (WIDTH // 2 - 9, HEIGHT // 2 + 130)

        # main game
        run = True
        show_score = False
        game_over = False

        while run:
            for event in pygame.event.get():
                if event.type == QUIT:
                    run = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if mole_rect.collidepoint(mouse_pos) and not game_over:
                            bonk.play()
                            current_sc += 1
                            score += 1
                            if score >= 5 and countdown <= 0:
                                score = 0
                                countdown = 5
                                current_level += 1
                                if current_level > 3:
                                    current_level = 3
                                    countdown = False
                                    game_over = True
                        hammer_img = hammer[1]
                        hammer_surface = pygame.transform.scale(hammer_img, (200, 200))
                        if not game_over:
                            pos = random_mole_position()
                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        hammer_img = hammer[0]
                        hammer_surface = pygame.transform.scale(hammer_img, (200, 200))
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        run = False
                mouse_pos = pygame.mouse.get_pos()
                hammer_rect.center = (mouse_pos[0], mouse_pos[1])

            now = pygame.time.get_ticks()
            if countdown > 0:
                if now - last_update > 1000:
                    last_update = now
                    countdown -= 1
                    if not game_over:
                        pos = random_mole_position()
                    screen.fill(BG)
                    draw_text(str(countdown), 40, WHITE, WIDTH//2, HEIGHT//2 - 10)
                else:
                    screen.fill(BG)
                    draw_text(str(countdown), 40, WHITE, WIDTH//2, HEIGHT//2 - 10)
            else:
                if not game_over:
                    if game_start_time == 0:
                        game_start_time = now
                    screen.fill(BG)
                    draw_text("Level {}".format(current_level), 40, WHITE, WIDTH // 2, 20)
                    draw_text("Score: {}".format(score), 30, WHITE, WIDTH // 2 - 40, HEIGHT // 2)
                    level_durations[current_level - 1] -= clock.get_time()
                    if level_durations[current_level - 1] <= 0 and score < 10:
                        game_over = True
                        last_update = now
                        current_level += 1
                        if current_level > 3:
                            game_over = True

                            if level_durations[current_level - 1] <= 0:
                                if score < 5:
                                    game_over = True
                                    last_update = now
                                else:
                                    if current_level == 3:
                                        game_over = True
            
            if now - last_mole_move > set_level_speed(current_level) and countdown == 0 and not game_over:
                pos = random_mole_position()
                last_mole_move = now

            if countdown == 0 and not game_over:
                screen.blit(mole, mole_rect)
                draw_land()

            if game_over:
                screen.fill(BG)
                draw_text("Game Over!", 40, WHITE, WIDTH // 2 - 100, HEIGHT // 2 - 60)
                # draw_text("Total Game Duration: {:.2f} seconds".format((game_start_time - game_over_time) / 1000), 30, WHITE, WIDTH // 2 - 180, HEIGHT // 2 - 20)
                draw_text("Click EXIT to quit", 30, WHITE, WIDTH // 2 - 100, HEIGHT // 2)
                screen.blit(exit_button, exit_button_rect)
                if exit_button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                    run = False
           
            draw_land()
            screen.blit(hammer_surface, hammer_rect)
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

def iterate():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-800/2, 800/2, -900/2,800/2)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def drawText(text,x,y,R,G,B):
    glPushMatrix()
    glColor3ub(R, G, B)
    glRasterPos2i(x,y)
    for i in str(text):
        c= ord(i)
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, c)
    glPopMatrix()

def button():
    glPushMatrix()

    glBegin(GL_POLYGON)
    glColor3ub(255, 255, 255)
    glVertex2f(-50, 50)
    glVertex2f(-50, -10)
    glVertex2f(50, -10)
    glVertex2f(50, 50)
    glEnd()
    
    glBegin(GL_POLYGON)
    glColor3ub(255, 255, 255)
    glVertex2f(-50, -30)
    glVertex2f(-50, -90)
    glVertex2f(50, -90)
    glVertex2f(50, -30)
    glEnd()

    glPopMatrix()

def main_menu():
    while True:
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if x > 340 and x < 450 and y > 250 and y < 290:
                        play()
                    if x > 340 and x < 450 and y > 300 and y < 350:
                        pygame.quit()
                        quit()

        glClearColor(0.0706, 0.6509, 0.1608, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        iterate()
        button()
        drawText('Whack-a-Mole', -80, 100, 255, 255, 255,)
        drawText('Start', -24, 10, 0, 0, 0,)
        drawText('Quit', -24, -70, 0, 0, 0,)

        pygame.display.flip()
        pygame.time.wait(1)

main_menu()