from config import cfg
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y):
        pygame.sprite.Sprite.__init__(self)
        self.x = player_x
        self.y = player_y
        self.player_size = cfg['player_size']
        self.player_speed = cfg['player_speed']
        self.player_rect = pygame.Rect((player_x, player_y, self.player_size, self.player_size))

    def player_move(self, x, y):
        """Function updates player's coordinates according to game state."""
        self.x = x
        self.y = y
        self.player_rect = pygame.Rect((x, y, self.player_size, self.player_size))
