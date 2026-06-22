import pygame
from typing import Tuple

class Player:
    def __init__(self, player_id: str, x: float, y: float, color: Tuple[int, int, int], is_local: bool = False):
        self.player_id = player_id
        self.x = x
        self.y = y
        self.color = color
        self.is_local = is_local
        self.velocity_x = 0
        self.velocity_y = 0
        self.size = 8

    def update(self, delta_time: float):
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time

    def draw(self, surface, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y
        
        pygame.draw.circle(surface, (80, 80, 80), 
                          (int(screen_x), int(screen_y)), 
                          self.size + 2)
        
        pygame.draw.circle(surface, self.color, 
                          (int(screen_x), int(screen_y)), 
                          self.size)
        
        if self.is_local:
            pygame.draw.circle(surface, (255, 255, 255), 
                              (int(screen_x), int(screen_y)), 
                              self.size + 4, 1)
