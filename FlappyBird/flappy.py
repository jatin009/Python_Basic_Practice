import pygame
import random

from pygame.locals import(
    RLEACCEL,
    KEYDOWN,
    K_ESCAPE,
    K_SPACE,
    QUIT
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
game_score = 0

ADD_PILLAR = pygame.USEREVENT + 1       # custom event to add pillars
pygame.time.set_timer(ADD_PILLAR, 1800)     # at every 1.8 sec
clock = pygame.time.Clock()


class Bird(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        image_surf = pygame.image.load("images/bird2.png").convert()
        self.surf = pygame.transform.scale(image_surf, (40, 25))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH//4, SCREEN_HEIGHT//2)
        )

    def update(self, keys_pressed):
        if keys_pressed[K_SPACE]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
            self.surf = pygame.image.load("images/bird1.png").convert()     # flying bird
        else:
            self.surf = pygame.image.load("images/bird3.png").convert()     # landing bird
            self.rect.move_ip(0, 3)


class Pillar(pygame.sprite.Sprite):

    def __init__(self, **kwargs):
        super().__init__()
        height = random.randint(200, 300)
        image_surf = pygame.image.load("images/pipe.png").convert()
        image_surf = pygame.transform.scale(image_surf, (100, height))
        self.surf = pygame.transform.flip(image_surf, False, True)      # Flipping the pipe upside down
        self.surf.set_colorkey([255, 255, 255], RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH+100, height//2)
        )

    def update(self):
        global game_score
        self.rect.move_ip(-5, 0)
        if self.rect.right <= 0:
            self.kill()
            game_score += 1


class LowerPillar(Pillar):

    def __init__(self):
        super(Pillar, self).__init__()      # python super property used
        height = random.randint(200, 250)
        image_surf = pygame.image.load("images/pipe.png").convert()
        self.surf = pygame.transform.scale(image_surf, (100, height))
        self.surf.set_colorkey([255, 255, 255], RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH+100, SCREEN_HEIGHT-height//2)
        )


class Background(pygame.sprite.Sprite):

    def __init__(self, **kwargs):
        super().__init__()
        image_surf = pygame.image.load(kwargs["img_path"]).convert()
        self.surf = pygame.transform.scale(image_surf, (kwargs["width"], kwargs["height"]))
        self.surf.set_colorkey([0, 0, 0], RLEACCEL)
        if not kwargs["bottom_portion"]:
            self.rect = self.surf.get_rect(center=(kwargs["width"] // 2, kwargs["height"] // 2))
        else:
            self.rect = self.surf.get_rect(center=(kwargs["width"] // 2, SCREEN_HEIGHT - kwargs["height"] // 2))


pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
background = Background(img_path="images/background.png", width=SCREEN_WIDTH, height=SCREEN_HEIGHT-50, bottom_portion=False)
ground = Background(img_path="images/ground.png", width=SCREEN_WIDTH, height=50, bottom_portion=True)
bird = Bird()

pillar_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(background)
all_sprites.add(ground)
all_sprites.add(bird)

pygame.mixer.music.load("sounds/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

move_up_sound = pygame.mixer.Sound("sounds/Rising_putter.ogg")
collision_sound = pygame.mixer.Sound("sounds/Collision.ogg")

running = True

while running:

    # Event Handling
    fly_high = False
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == ADD_PILLAR:
            pillar = Pillar()
            lower_pillar = LowerPillar()
            pillar_sprites.add(pillar)
            pillar_sprites.add(lower_pillar)
            all_sprites.add(pillar)
            all_sprites.add(lower_pillar)

        elif event.type == QUIT:
            running = False

    # Update state of game objects
    pressed_keys = pygame.key.get_pressed()
    bird.update(pressed_keys)
    pillar_sprites.update()

    # Rendering
    screen.fill([255, 255, 255])
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(bird, pillar_sprites):
        bird.kill()
        move_up_sound.stop()
        collision_sound.play()
        running = False

    pygame.display.flip()

    clock.tick(50)

print(f"Your game score: {game_score}")
