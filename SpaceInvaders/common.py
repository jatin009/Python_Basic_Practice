import pygame

from pygame.locals import(
    K_RIGHT,
    K_LEFT,
    RLEACCEL,
    KEYDOWN,
    KEYUP,
    K_ESCAPE,
    K_SPACE,
    QUIT
)

FIRE_ENEMY_BULLET = pygame.USEREVENT + 1
pygame.time.set_timer(FIRE_ENEMY_BULLET, 1800)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ENEMIES_IN_A_ROW = 10

ENEMY_TYPES_ROW_WISE = ["enemy1", "enemy2", "enemy2", "enemy3", "enemy3"]
ENEMY_KILLING_POINTS = {"enemy1": 30, "enemy2": 20, "enemy3": 10}

LEFT_POS_X = 250
ENEMY_UPDATE_COUNTER = 25
WHITE = (255, 255, 255)

ASSETS_PATH = "assets/"
IMAGE_PATH = ASSETS_PATH+"images/"
SOUND_PATH = ASSETS_PATH+"sounds/"