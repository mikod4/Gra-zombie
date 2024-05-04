import pygame
from config import cfg
from random import randint


class Particle:
    def __init__(self, zombie_type, x, y):
        self.color = cfg['enemy_' + zombie_type + '_color']
        self.enemy_size = cfg['enemy_' + zombie_type + '_size']
        self.x = x
        self.y = y
        self.duration = randint(cfg['min_particle_duration'], cfg['max_particle_duration'])
        self.velocity_x = randint(cfg['min_particle_velocity'], cfg['max_particle_velocity'] / 10 - 1)
        self.velocity_y = randint(cfg['min_particle_velocity'], cfg['max_particle_velocity'] / 10 - 1)
