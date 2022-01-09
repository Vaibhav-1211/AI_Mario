import pygame
import sys
from level import Level
from settings import *


# function where level start running for the actual game
def new():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background1, (0, 0))
        level.run()

        pygame.display.update()
        clock.tick(60)


def play(x, y):
    playtext = IntroFont.render("PLAY", True, (255, 255, 255))
    screen.blit(playtext, (x, y))


def quit(x, y):
    quittext = IntroFont.render("QUIT", True, (255, 255, 255))
    screen.blit(quittext, (x, y))


# Pygame setup
pygame.init()

screen_height = 704
screen_width = 1200
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

IntroFont = pygame.font.Font("freesansbold.ttf", 25)

level = Level(level_map, screen)

# changing title of the game window
pygame.display.set_caption('Mario')

# icon of the window
icon = pygame.image.load("graphics/Mario/mario.png")
pygame.display.set_icon(icon)

# menu of the game start here
while True:
    # screen.fill((4, 156, 216))

    # Background
    background = pygame.image.load('graphics/super_mario_bros.png')
    background1 = pygame.image.load('graphics/back.png')

    screen.blit(background1, (0, 0))
    screen.blit(background, (400, 200))

    play(screen_width / 2 - 170, screen_height / 2 + 100)
    quit(screen_width / 2 + 50, screen_height / 2 + 100)  # button text move

    x, y = pygame.mouse.get_pos()
    button1 = pygame.Rect(screen_width / 2 - 200, screen_height / 2 + 60, 130, 100)
    button2 = pygame.Rect(screen_width / 2 + 20, screen_height / 2 + 60, 130, 100)  # butteon grid move

    pygame.draw.rect(screen, (255, 255, 255), button1, 3)
    pygame.draw.rect(screen, (255, 255, 255), button2, 3)

    if button1.collidepoint(x, y):
        pygame.draw.rect(screen, (238, 69, 52), button1, 5)

    if button2.collidepoint(x, y):
        pygame.draw.rect(screen, (238, 69, 52), button2, 5)

    # click = False
    # key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if button1.collidepoint(x, y):
                print('inside')
                new()

            x, y = pygame.mouse.get_pos()
            if button2.collidepoint(x, y):
                pygame.quit()
                sys.exit()

    pygame.display.update()
    clock.tick(60)
