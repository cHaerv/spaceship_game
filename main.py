import pygame
import os
#import time
import random 


pygame.font.init()

# set up window for display
WIDTH, HEIGHT = 800, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Port Defense")

#colours
WHITE = (255,255,255)

#load assets 
PLAYER_SHIP = pygame.image.load(os.path.join("assets", "player_ship.png"))

CRAB_SHIP = pygame.image.load(os.path.join("assets", "crab_ship.png"))
EI_SHIP = pygame.image.load(os.path.join("assets", "ei_ship.png"))
MANTA_SHIP = pygame.image.load(os.path.join("assets", "manta_ship.png"))
TELHAARI_SHIP = pygame.image.load(os.path.join("assets", "telhari_ship.png"))

BACK_GROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")), (WIDTH, HEIGHT))


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


#player class will inherit from Ship 
class Player(Ship):
    def __init__(self, x, y, health=100):
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
    def __init__(self, x, y, alien,  health=10):
        super().__init__(x, y, health)
        self.ship_img = self.ALIEN_MAP[alien]
        self.projectile_1 = self.BULLET_MAP[alien]
        self.mask = pygame.mask.from_surface(self.ship_img) # makes the hitbox relative to coloured pixels

    def move(self, vel):
        self.y += vel

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
    
def collide(obj_1, obj_2):
    offset_x = obj_2.x -obj_1.x
    offset_y = obj_1.y - obj_2.y
    return obj_1.mask.overlap(obj_2.mask, (offset_x, offset_y)) != None



def main():
    running = True 
    FPS = 60
    level = 0
    lives = 5
    defeat = False
    defeat_timer = 0
    my_font = pygame.font.SysFont("Arial", 30)
    player_vel = 5
    projectile_vel = 6

    clock = pygame.time.Clock()

    enemies = [] #list of enemies
    enemies_per_wave = 5 #how many enemies
    enemy_vel = 1

    player = Player(300,650)

    def redraw_window():
        WIN.blit(BACK_GROUND, (0,0))
        lives_tally = my_font.render(f"lives: {lives}", 1, WHITE)
        level_tally = my_font.render(f"Level: {level}", 1, WHITE)

        WIN.blit(lives_tally, (10,10))
        WIN.blit(level_tally, (WIDTH - level_tally.get_width() - 10, 10))
        
        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if defeat:
            defeat_screen = my_font.render("Defeat!", 1, (255, 0, 0))
            WIN.blit(defeat_screen, (WIDTH/2 - defeat_screen.get_width()/2, 350))



        pygame.display.update()

        
    while running:
        clock.tick(FPS)
        redraw_window() #will redraw the window every frame


        if lives <= 0 or player.health <= 0:
            defeat = True
            defeat_timer += 1

        if defeat:
            if defeat_timer > 4 * FPS:
                running = False
            else:
                continue
            
        
        #spawns enemies
        if len(enemies) == 0:
            level += 1
            enemies_per_wave += 5 #adds this many enemies per wave
            for i in range(enemies_per_wave):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["crab", "ei", "manta", "telhaari"]))
                enemies.append(enemy)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #gets keys pressed and controls player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: #left
            player.x -= player_vel 
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: #right
            player.x += player_vel 
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT: #down
            player.y += player_vel 
        if keys[pygame.K_w] and player.y - player_vel > 0: #up
            player.y -= player_vel 
        if keys[pygame.K_SPACE]:
            player.fire()
        
        for enemy in enemies:
            enemy.move(enemy_vel) #moves enemies
            enemy.move_projectiles(projectile_vel, player)
            if random.randrange(0,500) == 1:
                enemy.fire()

            if collide(enemy, player):
                player.health -= 5
                enemies.remove(enemy)

            if enemy.y > HEIGHT:
                enemies.remove(enemy) #removes them if they get pas the player and decrements your health
                lives -= 1
            
        player.move_projectiles(-projectile_vel, enemies)


        
    

if __name__ == '__main__':
    main()