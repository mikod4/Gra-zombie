import pygame
from config import cfg
from random import randint


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_x, enemy_y):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'normal'
        self.speed = cfg['enemy_normal_speed']
        self.x = enemy_x
        self.y = enemy_y
        self.size = cfg['enemy_normal_size']
        self.value = cfg['enemy_normal_value']
        self.health = randint(cfg['enemy_normal_min_health'], cfg['enemy_normal_max_health'])
        self.enemy_color = cfg['enemy_normal_color']
        self.enemy_rect = pygame.Rect((self.x, self.y, self.size, self.size))
        self.font = pygame.font.Font(cfg['font_name'], 10)
        self.health_text = self.font.render(
            str(self.health), True, (0, 0, 0), self.enemy_color
        )

    def move_to_player(self, player_x, player_y):
        """Function is moving enemy towards player coordinates."""
        if self.x != player_x and self.y != player_y:
            self.speed = cfg['enemy_normal_speed'] / 1.41
        else:
            self.speed = cfg['enemy_normal_speed']

        if player_x > self.x:
            self.x += self.speed
        elif player_x < self.x:
            self.x -= self.speed

        if player_y > self.y:
            self.y += self.speed
        elif player_y < self.y:
            self.y -= self.speed

        self.y = round(self.y, 0)
        self.x = round(self.x, 0)

        self.enemy_rect = pygame.Rect((self.x, self.y, self.size, self.size))

    def remove_health(self, bullet_damage):
        """Function removes enemy health. If enemy has no health left it returns false else ture"""
        self.health -= bullet_damage
        self.health_text = self.font.render(
            str(self.health), True, (0, 0, 0), self.enemy_color
        )
        if self.health <= 0:
            return False
        return True
