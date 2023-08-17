import pygame
import random 
from dino_runner.components.obstacles.cactus import Cactus 
from dino_runner.components.obstacles.bird import Bird


class ObstacleManager:

    def __init__(self):
        self.obstacles = []

    def update(self, game): # atualiza os obstacles
        image_list = [Cactus(), Bird()]
        if len(self.obstacles) == 0:
            self.obstacles.append(image_list[random.randint(0,1)])
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles) #como arrgumento 
            if game.player.dino_rect.colliderect(obstacle.rect):# se houver uma colisao
                if not game.player.has_power_up:
                    pygame.time.delay(500) #cria um pequeno atraso 
                    game.death_count += 1
                    game.playing = False 
                    
                    
                    break
                else: 
                    self.obstacles.remove(obstacle)

    def reset_obstacles(self):#redefine a lista de obstáculos
        self.obstacles = []   # usado quando o jogo está sendo reiniciado

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
               
      