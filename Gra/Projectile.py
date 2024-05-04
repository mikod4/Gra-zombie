import pygame
from config import cfg


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.size = cfg['projectile_size']
        self.direction = direction
        self.range = cfg['projectile_range']
        self.speed = cfg['projectile_speed']
        self.damage = cfg['projectile_damage']
        self.projectile_rect = pygame.Rect((self.x, self.y, self.size, self.size))

    def travel(self):
        """Function handles bullet movement meaning if it was shot right bullet will travel only right
        and so on."""
        match self.direction:
            case "up":
                self.y -= self.speed
                self.projectile_rect = pygame.Rect(
                    (self.x, self.y, self.size, self.size)
                )

            case "down":
                self.y += self.speed
                self.projectile_rect = pygame.Rect(
                    (self.x, self.y, self.size, self.size)
                )

            case "left":
                self.x -= self.speed
                self.projectile_rect = pygame.Rect(
                    (self.x, self.y, self.size, self.size)
                )

            case "right":
                self.x += self.speed
                self.projectile_rect = pygame.Rect(
                    (self.x, self.y, self.size, self.size)
                )

