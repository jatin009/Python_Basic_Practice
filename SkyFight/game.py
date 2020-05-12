import pygame
import random

from pygame.locals import(
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

ADD_ENEMY = pygame.USEREVENT + 1    # custom event for enemy creation
pygame.time.set_timer(ADD_ENEMY, 250)

ADD_CLOUD = pygame.USEREVENT + 2    # custom event for cloud creation
pygame.time.set_timer(ADD_CLOUD, 1000)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    """
    Representing player sprite object. The surface drawn on the screen is now an attribute of 'player'
    """
    def __init__(self):
        super(Player, self).__init__()      # TODO: Read supercharging in python
        # pygame.image.load will get you a surface like pygame.Surface((75, 25))
        self.surf = pygame.image.load("jet.png").convert()
        # self.surf = pygame.transform.scale(self.surf, (75, 25))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        # self.surf.fill((0, 0, 0))       # filled with black color, not reqd with image loads
        self.rect = self.surf.get_rect()

    def update(self, keys_pressed):
        if keys_pressed[K_UP]:
            if self.rect.top >= 5:
                self.rect.move_ip(0, -5)
                move_up_sound.play()
        elif keys_pressed[K_DOWN]:
            if self.rect.bottom <= SCREEN_HEIGHT-5:
                self.rect.move_ip(0, 5)
                move_down_sound.play()
        elif keys_pressed[K_RIGHT]:
            if self.rect.right <= SCREEN_WIDTH-5:
                self.rect.move_ip(5, 0)
        elif keys_pressed[K_LEFT]:
            if self.rect.left >= 5:
                self.rect.move_ip(-5, 0)


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("missile.png").convert()
        # self.surf = pygame.transform.scale(self.surf, (20, 10))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        # setting origin point
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                random.randint(5, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(7, 20)      # enemy sprite movement speed

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right <= 0:        # kill once it disappears
            self.kill()


class Cloud(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey([0, 0, 0], RLEACCEL)     # set this color same as background color of image
        self.rect = self.surf.get_rect(
            center =
            (
                random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

    def update(self, *args):
        self.rect.move_ip(-5, 0)
        if self.rect.right <= 0:
            self.kill()


pygame.init()       # initializing pygame modules like display, joystick etc

# creating display object and returning Surface
screen = pygame.display.set_mode(size=[SCREEN_WIDTH, SCREEN_HEIGHT])
player = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

running = True

while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # Escape key pressed
            if event.key == K_ESCAPE:
                running = False

        # Window close button pressed
        elif event.type == QUIT:
            running = False

        elif event.type == ADD_ENEMY:
            enemy = Enemy()
            enemies.add(enemy)
            all_sprites.add(enemy)
            
        elif event.type == ADD_CLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # Get pressed keys and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update enemies and clouds sprites
    enemies.update()
    clouds.update()

    screen.fill((135, 206, 250))       # fill screen with sky color, has to be before blitting
    # Drawing all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False
        move_down_sound.stop()
        move_up_sound.stop()
        collision_sound.play()

    pygame.display.flip()

    clock.tick(30)
