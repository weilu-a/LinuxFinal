import os
from typing import List, Tuple

TILE_FLOOR = 0
TILE_WALL = 1


class GridWorld:
    def __init__(self, map_file, tile_size=32):
        self.tile_size = tile_size
        self.grid = []
        self.width = 0
        self.height = 0
        self.load_map(map_file)

    def load_map(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Map file not found: {filepath}")

        with open(filepath, 'r') as f:
            lines = f.readlines()

        lines = [line.strip() for line in lines if line.strip()]

        if not lines:
            raise ValueError("Empty map file")

        original_width = len(lines[0])
        original_height = len(lines)

        for line in lines:
            if len(line) != original_width:
                raise ValueError("Map lines have inconsistent length")

        self.width = original_width + 2
        self.height = original_height + 2

        self.grid = []

        self.grid.append([TILE_WALL] * self.width)

        for y, line in enumerate(lines):
            row = [TILE_WALL]
            for x, char in enumerate(line):
                try:
                    tile = int(char)
                except ValueError:
                    tile = TILE_FLOOR

                row.append(tile)

            row.append(TILE_WALL)
            self.grid.append(row)

        self.grid.append([TILE_WALL] * self.width)

    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return TILE_WALL

    def is_wall(self, x, y):
        return self.get_tile(x, y) == TILE_WALL

    def is_walkable(self, x, y):
        tile = self.get_tile(x, y)
        return tile != TILE_WALL

    def get_world_size(self):
        return self.width * self.tile_size, self.height * self.tile_size

    def render(self, surface, camera):
        import pygame

        cam_x = int(camera.x)
        cam_y = int(camera.y)

        view_width = int(camera.width / self.tile_size) + 3
        view_height = int(camera.height / self.tile_size) + 3

        start_x = max(0, int(cam_x / self.tile_size) - 1)
        start_y = max(0, int(cam_y / self.tile_size) - 1)

        end_x = min(self.width, start_x + view_width)
        end_y = min(self.height, start_y + view_height)

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.get_tile(x, y)
                screen_x = x * self.tile_size - cam_x
                screen_y = y * self.tile_size - cam_y

                if -self.tile_size <= screen_x <= camera.width and \
                   -self.tile_size <= screen_y <= camera.height:
                    if tile == TILE_WALL:
                        pygame.draw.rect(surface, (100, 100, 100),
                                        (screen_x, screen_y, self.tile_size, self.tile_size))
                        pygame.draw.rect(surface, (130, 130, 130),
                                        (screen_x + 2, screen_y + 2, self.tile_size - 4, self.tile_size - 4))
                    else:
                        pygame.draw.rect(surface, (60, 60, 60),
                                        (screen_x, screen_y, self.tile_size, self.tile_size))
                        if (x + y) % 2 == 0:
                            pygame.draw.rect(surface, (55, 55, 55),
                                            (screen_x, screen_y, self.tile_size, self.tile_size))
