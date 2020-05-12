from common import *
from missile import Ship, Enemy, StaticSprite, Text, Sounds
import random


class SpaceInvaders:
    def __init__(self):
        pygame.init()
        # Creating game variables
        self.screen = pygame.display.set_mode([800, 600])
        self.ship = Ship()
        self.enemies = pygame.sprite.Group()
        self.all_entities = pygame.sprite.Group()
        self.enemies_bullets = pygame.sprite.Group()
        self.background = StaticSprite("assets/images/background.jpg", None, center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        # Initializing game object variables
        self.running = True
        self.sounds = Sounds()
        self.enemy_update_counter = ENEMY_UPDATE_COUNTER
        for row_num, enemy_type in enumerate(ENEMY_TYPES_ROW_WISE):
            for col_num in range(ENEMIES_IN_A_ROW):
                enemy = Enemy(enemy_type, row_num, col_num)
                self.enemies.add(enemy)
                self.all_entities.add(enemy)
        self.all_entities.add(self.ship)
        # Score board
        self.score_points = 0
        self.lives = 3
        self.life_icons = []

    def game_loop(self):
        show_start_screen = True
        text1 = Text('SPACE INVADERS', 50, WHITE, center=(400, 200))
        text2 = Text('PRESS ANY KEY TO CONTINUE', 25, WHITE, center=(400, 300))
        score_text = Text(f'SCORE: {self.score_points}', 20, WHITE, topleft=(5, 5))
        lives_text = Text(f'LIVES: ', 20, WHITE, topright=(SCREEN_WIDTH-75, 5))

        for life in range(self.lives):
            life_sprite = StaticSprite("assets/images/ship.png", (22, 22), topright=(SCREEN_WIDTH-5-25*life, 5))
            self.life_icons.append(life_sprite)

        while self.running:
            if show_start_screen:
                # Event Handling
                for event in pygame.event.get():
                    if event.type == KEYUP:
                        show_start_screen = False
                    elif event.type == QUIT:
                        self.running = False
                self.screen.blit(self.background.surf, self.background.rect)
                self.screen.blit(text1.surf, text1.rect)
                self.screen.blit(text2.surf, text2.rect)
            else:
                self.fighting_loop(score_text=score_text, lives_text=lives_text)
            pygame.display.flip()

    def fighting_loop(self, **kwargs):
        # Event Handling
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False

                elif event.key == K_SPACE:
                    if not self.ship.bullet:  # no other bullet should be fired until previous one hits/disappears
                        self.ship.fire_bullet()
                        self.sounds.ship_bullet_sound.play()
                        self.all_entities.add(self.ship.bullet)

            elif event.type == FIRE_ENEMY_BULLET:
                enemies_list = self.enemies.sprites()
                # Choosing a random enemy to fire a bullet
                random_enemy = enemies_list[random.randint(0, len(enemies_list) - 1)]
                random_enemy.fire_bullet()
                self.enemies_bullets.add(random_enemy.enemy_bullet)
                self.all_entities.add(random_enemy.enemy_bullet)

            elif event.type == QUIT:
                self.running = False

        # Updating game objects (Game Logic)
        pressed_keys = pygame.key.get_pressed()
        self.ship.update(pressed_keys)
        self.enemies_bullets.update()

        self.enemy_update_counter -= 1
        if self.enemy_update_counter == 0:
            self.enemies.update()
            self.sounds.enemy_moving_sound.play()
            self.enemy_update_counter = ENEMY_UPDATE_COUNTER

        # If it's enemy_bullet-ship collision, destroy both of them right away and end the game
        if pygame.sprite.spritecollide(self.ship, self.enemies_bullets, True):
            self.lives -= 1
            self.life_icons.pop(self.lives)
            self.sounds.ship_killed_sound.play()
            if self.lives == 0:
                self.running = False
                self.ship.kill()

        if self.ship.bullet:  # no need to update if bullet never fired
            # False for not killing the enemy right away, we want to show it destroyed
            enemy_sprite = pygame.sprite.spritecollide(self.ship.bullet, self.enemies, False)
            # If it's bullet-bullet collision, destroy both of them right away
            if pygame.sprite.spritecollide(self.ship.bullet, self.enemies_bullets, True):
                self.ship.bullet.update(target_hit=True)
            elif enemy_sprite:  # bullet hit the enemy
                enemy_sprite[0].hit_by_bullet()
                self.score_points += ENEMY_KILLING_POINTS[enemy_sprite[0].enemy_type]   # Update score points
                self.sounds.enemy_killed_sound.play()
                self.ship.bullet.update(target_hit=True)
            else:
                self.ship.bullet.update()
            self.ship.update_bullet_status()

        # Rendering (Game View)
        self.screen.blit(self.background.surf, self.background.rect)
        for entity in self.all_entities:
            self.screen.blit(entity.surf, entity.rect)
        # Rendering Game Score
        kwargs['score_text'].update(f'SCORE: {self.score_points}', WHITE)
        self.screen.blit(kwargs['score_text'].surf, kwargs['score_text'].rect)
        # Rendering Ship Lives
        self.screen.blit(kwargs['lives_text'].surf, kwargs['lives_text'].rect)
        for life in self.life_icons:
            self.screen.blit(life.surf, life.rect)


game_obj = SpaceInvaders()
game_obj.game_loop()
