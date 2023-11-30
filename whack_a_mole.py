import pygame, sys
from button import Button
import os
import random

from os import path
from pygame.locals import *

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
audio_folder = os.path.join(game_folder, 'audio')

pygame.init()

SCREEN = pygame.display.set_mode((800,600))
pygame.display.set_caption('Menu')

BG = pygame.image.load(path.join(img_folder, 'land.png'))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(path.join(img_folder, 'Roboto-Regular.ttf'))

def play():
    pygame.display.set_caption("Play")

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

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

        def set_level_speed(level):
            speeds = [3000, 2000, 1000]
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
        level_durations = [0,10, 10, 10]
        current_level = 1
        last_update = pygame.time.get_ticks()
        score = 0
        last_mole_move = pygame.time.get_ticks()

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
                            score += 1
                        hammer_img = hammer[1]
                        hammer_surface = pygame.transform.scale(hammer_img, (200, 200))
                        if not game_over:
                            random_mole_position()
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
                        random_mole_position()
                    screen.fill(BG)
                    draw_text(str(countdown), 40, WHITE, WIDTH//2, 20)
                else:
                    screen.fill(BG)
                    draw_text(str(countdown), 40, WHITE, WIDTH//2, 20)
            else:
                if now - last_update < level_durations[current_level] * 1000:
                    screen.fill(BG)
                    draw_text(str(level_durations[current_level] - int((now - last_update) / 1000)), 40, WHITE, WIDTH//2, 20)
                else:

                    last_update = now
                    countdown = 5
                    current_level += 1
                    if current_level == 1:
                        level_duration = 10
                    elif current_level == 2:
                        level_duration = 15
                    elif current_level == 3:
                        level_duration = 20
                    elif current_level == 4:
                        game_over = True
                        countdown = 1000
            if now - last_mole_move > set_level_speed(current_level) and countdown == 0 and not game_over:
                random_mole_position()
                last_mole_move = now

            if countdown == 0:
                screen.blit(mole, mole_rect)
                draw_land()

            if game_over:
                screen.fill(BG)
                draw_text("Skor: {}".format(score), 40, WHITE, WIDTH//2 - 60, HEIGHT//2 - 60)
                draw_text("klik EXIT untuk keluar", 30, BLACK, WIDTH//2 - 120, HEIGHT//2 )

            # Gambar tombol keluar
                screen.blit(exit_button, exit_button_rect)

            # Periksa klik tombol keluar
                if exit_button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                    run = False

            draw_land()
            screen.blit(hammer_surface, hammer_rect)
            pygame.display.flip()
            clock.tick(FPS)


        pygame.quit()





def main_menu():
    pygame.display.set_caption("Menu")

    while True:
        SCREEN.blit(BG, (0,0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 200))

        PLAY_BUTTON = Button(image=None, pos=(400,250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="orange")
        QUIT_BUTTON = Button(image=None, pos=(400,300),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="orange")
        
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()