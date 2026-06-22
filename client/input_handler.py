import pygame
from typing import Tuple

class InputHandler:
    def __init__(self):
        pass

    def get_movement_vector(self, keys) -> Tuple[float, float]:
        dx = 0.0
        dy = 0.0
        
        if keys[pygame.K_w]:
            dy = -1.0
        if keys[pygame.K_s]:
            dy = 1.0
        if keys[pygame.K_a]:
            dx = -1.0
        if keys[pygame.K_d]:
            dx = 1.0
        
        length = (dx ** 2 + dy ** 2) ** 0.5
        if length > 0:
            dx /= length
            dy /= length
        
        return dx, dy
