import pygame
from config import cfg
from random import randint
from math import floor


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_x, enemy_y):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'charger'
        self.speed = cfg['enemy_charger_speed']
        self.x = enemy_x
        self.y = enemy_y
        self.size = cfg['enemy_charger_size']
        self.value = cfg['enemy_charger_value']
        self.health = randint(cfg['enemy_charger_min_health'], cfg['enemy_charger_max_health'])
        self.enemy_color = cfg['enemy_charger_color']
        self.enemy_rect = pygame.Rect((self.x, self.y, self.size, self.size))
        self.font = pygame.font.Font(cfg['font_name'], 10)
        self.health_text = self.font.render(
            str(self.health), True, (0, 0, 0), self.enemy_color
        )

    def move_to_player(self, player_x, player_y):
        """Function is moving enemy towards player coordinates. And handles Charger's ability to
        increase speed if charger's coordinates are equal to player coordinates."""
        player_x = floor(player_x)
        player_y = floor(player_y)
        if floor(self.x) == player_x or floor(self.y) == player_y:
            self.speed += cfg['enemy_charger_charge_speed']
            self.enemy_color = cfg['enemy_charger_charge_color']
            self.health_text = self.font.render(
                str(self.health), True, (0, 0, 0), self.enemy_color
            )
        else:
            self.enemy_color = cfg['enemy_charger_color']
            self.health_text = self.font.render(
                str(self.health), True, (0, 0, 0), self.enemy_color
            )

        if floor(self.x) != player_x and floor(self.y) != player_y:
            self.speed = cfg['enemy_charger_speed'] / 1.41
        else:
            self.speed = cfg['enemy_charger_speed']

        if player_x > floor(self.x):
            self.x += self.speed
        elif player_x < floor(self.x):
            self.x -= self.speed

        if player_y > floor(self.y):
            self.y += self.speed
        elif player_y < floor(self.y):
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
