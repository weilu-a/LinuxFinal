class Camera:
    def __init__(self, width, height, world_width, world_height):
        self.width = width
        self.height = height
        self.world_width = world_width
        self.world_height = world_height
        
        self.x = max(0, (world_width - width) / 2)
        self.y = max(0, (world_height - height) / 2)
