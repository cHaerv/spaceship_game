import pygame
import os
from .ship import Ship

CRAB_SHIP = pygame.image.load(os.path.join("assets", "crab_ship.png"))
EI_SHIP = pygame.image.load(os.path.join("assets", "ei_ship.png"))
MANTA_SHIP = pygame.image.load(os.path.join("assets", "manta_ship.png"))
TELHAARI_SHIP = pygame.image.load(os.path.join("assets", "telhari_ship.png"))

class Enemy(Ship):
    #different forms of vessels 
    ALIEN_MAP = {
        "crab": (CRAB_SHIP),
        "ei": (EI_SHIP),
        "manta": (MANTA_SHIP),
        "telhaari": (TELHAARI_SHIP)

    }
    BULLET_MAP = {
        "crab": (pygame.image.load(os.path.join("assets", "crab_projectile.png"))),
        "ei": (pygame.image.load(os.path.join("assets", "crab_projectile.png"))),
        "manta": (pygame.image.load(os.path.join("assets", "crab_projectile.png"))),
        "telhaari": (pygame.image.load(os.path.join("assets", "crab_projectile.png")))
    }

    def __init__(self, x, y, alien,  health=50):
        super().__init__(x, y, health)
        self.ship_img = self.ALIEN_MAP[alien]
        self.projectile_1 = self.BULLET_MAP[alien]
        self.mask = pygame.mask.from_surface(self.ship_img) # makes the hitbox relative to coloured pixels

    def move(self, vel):
        self.y += vel
