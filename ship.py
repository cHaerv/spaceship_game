import pygame
from projectile import Projectile

WIDTH, HEIGHT = 800, 750

#generic class for creating players and enemies
class Ship:
    COOLDOWN = 20 
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.projectile_1 = None
        self.projectiles = []
        self.cool_down_counter = 0
        
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for projectile in self.projectiles:
            projectile.draw(window)

    
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()
    
    def fire(self):
        if self.cool_down_counter == 0:
            projectiles = Projectile(self.x, self.y, self.projectile_1)
            self.projectiles.append(projectiles)
            self.cool_down_counter = 1

    def move_projectiles(self, vel, obj):
        self.cooldown()
        for projectile in self.projectiles:
            projectile.move(vel)
            if projectile.gone(HEIGHT):
                self.projectiles.remove(projectile)
            elif projectile.hit(obj):
                obj.health -= 10
                self.projectiles.remove(projectile)


    
