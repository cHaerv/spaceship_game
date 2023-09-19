import pygame
from ship import Ship
import os

PLAYER_SHIP = pygame.image.load(os.path.join("assets", "player_ship.png"))
WIDTH, HEIGHT = 800, 750

#player class will inherit from Ship 
class Player(Ship):
    def __init__(self, x, y, health=50):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SHIP
        self.projectile_1 = pygame.image.load(os.path.join("assets", "player_projectile.png"))
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_projectiles(self, vel, objs):
        self.cooldown()
        for projectile in self.projectiles:
            projectile.move(vel)
            if projectile.gone(HEIGHT):
                self.projectiles.remove(projectile)
            else:
                for obj in objs:
                    if projectile.hit(obj):
                        objs.remove(obj)
                        obj.health -= 10
                        self.projectiles.remove(projectile)
    
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
    
    
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 5))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 5))