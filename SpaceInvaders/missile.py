from common import *
import enum


class MotionDirection(enum.Enum):
    """
    Enemy Motion Direction
    """
    LEFT = 1,
    RIGHT = 2


class Sounds:
    def __init__(self):
        self.enemy_moving_sound = pygame.mixer.Sound("assets/sounds/0.wav")
        self.ship_bullet_sound = pygame.mixer.Sound("assets/sounds/shoot.wav")
        self.enemy_killed_sound = pygame.mixer.Sound("assets/sounds/invaderkilled.wav")
        self.ship_killed_sound = pygame.mixer.Sound("assets/sounds/shipexplosion.wav")


class Text:
    def __init__(self, font_text, font_size, color, **kwargs):
        self.game_font = pygame.font.Font("assets/fonts/space_invaders.ttf", font_size)
        self.surf = self.game_font.render(font_text, True, color)
        self.rect = self.surf.get_rect(**kwargs)

    def update(self, font_text, color):
        self.surf = self.game_font.render(font_text, True, color)


class StaticSprite(pygame.sprite.Sprite):
    """
    For loading static images like Background png and Ship icons for remaining lives.
    """
    def __init__(self, img_path, size, **kwargs):
        super().__init__()
        self.surf = pygame.image.load(img_path)
        self.surf.set_colorkey(WHITE, RLEACCEL)
        if size is not None:
            self.surf = pygame.transform.scale(self.surf, size)
        self.rect = self.surf.get_rect(**kwargs)


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("assets/images/ship.png")
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect(center=(350, 550))
        self.bullet = None

    def update(self, keys_pressed):
        if keys_pressed[K_RIGHT]:
            if self.rect.right <= SCREEN_WIDTH-5:
                self.rect.move_ip(5, 0)
        elif keys_pressed[K_LEFT]:
            if self.rect.left >= 5:
                self.rect.move_ip(-5, 0)

    def fire_bullet(self):
        self.bullet = ShipBullet(self.rect)

    def update_bullet_status(self):
        if not self.bullet.in_motion:
            self.bullet = None


class Bullet(pygame.sprite.Sprite):
    """
    Base class for ship and enemy bullets
    """
    def __init__(self, laser_type, pos_rect):
        super().__init__()
        self.surf = pygame.image.load(f"assets/images/{laser_type}_laser.png")
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect(center=(pos_rect.centerx, pos_rect.centery))


class ShipBullet(Bullet):
    def __init__(self, pos_rect):
        super().__init__("player", pos_rect)
        self.in_motion = True
        self.speed = -15

    def update(self, target_hit=False):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom < 0 or target_hit:
            self.in_motion = False
            self.kill()


class EnemyBullet(Bullet):
    def __init__(self, pos_rect):
        super().__init__("enemy", pos_rect)
        self.speed = 8

    def update(self, target_hit=False):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > SCREEN_HEIGHT or target_hit:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, row_idx, col_idx):
        super().__init__()
        self.enemy_type = enemy_type
        self.images = {"standing": f"assets/images/{self.enemy_type}_1.png",
                       "moving": f"assets/images/{self.enemy_type}_2.png",
                       "destroyed": f"assets/images/{self.enemy_type}_explosion.png"}
        self.current_img = self.images["standing"]
        image_surf = pygame.image.load(self.current_img)
        self.surf = pygame.transform.scale(image_surf, (40, 35))
        self.surf.set_colorkey(WHITE, RLEACCEL)

        # attributes for going down by 1 row
        self.left_offset = col_idx * 50
        self.right_offset = (ENEMIES_IN_A_ROW-1-col_idx) * 50
        self.rect = self.surf.get_rect(center=(LEFT_POS_X + self.left_offset, 100 + row_idx*45))
        self.alive = True
        self.motion_direction = MotionDirection.LEFT
        self.enemy_bullet = None

    def fire_bullet(self):
        self.enemy_bullet = EnemyBullet(self.rect)

    def load_image(self):
        image_surf = pygame.image.load(self.current_img)
        self.surf = pygame.transform.scale(image_surf, (40, 35))

    def hit_by_bullet(self):
        self.alive = False
        self.current_img = self.images["destroyed"]
        self.load_image()

    def toggle_image(self):
        self.current_img = self.images["moving"] \
            if self.current_img == self.images["standing"] \
            else self.images["standing"]
        self.load_image()

    def update(self):
        if self.alive:
            if self.motion_direction == MotionDirection.LEFT:
                if self.rect.left >= 10+self.left_offset:
                    self.rect.move_ip(-10, 0)
                    self.toggle_image()
                else:
                    self.motion_direction = MotionDirection.RIGHT
                    self.rect.move_ip(0, 20)
            else:
                if self.rect.right <= SCREEN_WIDTH - 10-self.right_offset:
                    self.rect.move_ip(10, 0)
                    self.toggle_image()
                else:
                    self.motion_direction = MotionDirection.LEFT
                    self.rect.move_ip(0, 20)
        else:
            self.kill()
