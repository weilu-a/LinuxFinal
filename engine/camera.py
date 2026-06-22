import pygame

class Camera:
    def __init__(self, width, height, world_width, world_height, boundary_margin=0):
        self.width = width
        self.height = height
        self.world_width = world_width
        self.world_height = world_height
        self.boundary_margin = boundary_margin
        
        self.x = 0
        self.y = 0
        
        self.target_x = 0
        self.target_y = 0
        
        self.speed = 0.15
        self.move_speed = 300
        
        self.dragging = False
        self.last_mouse_pos = (0, 0)
    
    def update(self, keys, delta_time):
        self.target_x += (keys[pygame.K_d] - keys[pygame.K_a]) * self.move_speed * delta_time
        self.target_y += (keys[pygame.K_s] - keys[pygame.K_w]) * self.move_speed * delta_time
        
        self.x += (self.target_x - self.x) * self.speed
        self.y += (self.target_y - self.y) * self.speed
        
        min_x = -self.boundary_margin
        max_x = self.world_width - self.width + self.boundary_margin
        min_y = -self.boundary_margin
        max_y = self.world_height - self.height + self.boundary_margin
        
        self.x = max(min_x, min(self.x, max_x))
        self.y = max(min_y, min(self.y, max_y))
    
    def handle_mouse_down(self, pos):
        self.dragging = True
        self.last_mouse_pos = pos
    
    def handle_mouse_up(self):
        self.dragging = False
    
    def handle_mouse_motion(self, pos):
        if self.dragging:
            dx = pos[0] - self.last_mouse_pos[0]
            dy = pos[1] - self.last_mouse_pos[1]
            
            self.target_x -= dx
            self.target_y -= dy
            
            min_x = -self.boundary_margin
            max_x = self.world_width - self.width + self.boundary_margin
            min_y = -self.boundary_margin
            max_y = self.world_height - self.height + self.boundary_margin
            
            self.target_x = max(min_x, min(self.target_x, max_x))
            self.target_y = max(min_y, min(self.target_y, max_y))
            
            self.last_mouse_pos = pos