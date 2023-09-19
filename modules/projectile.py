import pygame
from .collide import collide

class Projectile:
    def __init__(self, x, y, bullet):
        self.x = x
        self.y = y
        self.bullet = bullet
        self.mask = pygame.mask.from_surface(self.bullet)
    
    def draw(self, window):
        window.blit(self.bullet, (self.x, self.y))

    def move(self, vel):
        self.y += vel
    
    def gone(self, height):
        return not(self.y  < height and self.y >= 0)
    
    def hit(self, obj):
        return collide(obj, self)