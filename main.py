import pygame
import os
#import time
import random 
from modules import Ship, Projectile, collide, Player, Enemy

pygame.font.init()

# set up window for display
WIDTH, HEIGHT = 800, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Port Defense")

#colours
WHITE = (255,255,255)

BACK_GROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")), (WIDTH, HEIGHT))


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
            elif enemy.y > HEIGHT:
                enemies.remove(enemy) #removes them if they get pas the player and decrements your health
                lives -= 1
              
        player.move_projectiles(-projectile_vel, enemies)


        
    

if __name__ == '__main__':
    main()