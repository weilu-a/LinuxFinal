import os
from typing import Dict, List, Tuple

TILE_FLOOR = 0
TILE_WALL = 1

TILE_EVENT_STAND_NPC1 = 2
TILE_EVENT_STAND_NPC2 = 3
TILE_EVENT_STAND_NPC3 = 4
TILE_EVENT_EAT_MEAL = 5
TILE_EVENT_EAT_SNACK = 6
TILE_EVENT_SLEEP_DEEP = 7
TILE_EVENT_SLEEP_NAP = 8

TILE_TO_EVENT_ID = {
    TILE_EVENT_STAND_NPC1: 'stand_npc1',
    TILE_EVENT_STAND_NPC2: 'stand_npc2',
    TILE_EVENT_STAND_NPC3: 'stand_npc3',
    TILE_EVENT_EAT_MEAL: 'eat_meal',
    TILE_EVENT_EAT_SNACK: 'eat_snack',
    TILE_EVENT_SLEEP_DEEP: 'sleep_deep',
    TILE_EVENT_SLEEP_NAP: 'sleep_nap',
}


class GridWorld:
    def __init__(self, map_file, tile_size=32):
        self.tile_size = tile_size
        self.grid = []
        self.width = 0
        self.height = 0
        self.event_positions: Dict[str, List[Tuple[int, int]]] = {}
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
        self.event_positions = {}

        self.grid.append([TILE_WALL] * self.width)

        for y, line in enumerate(lines):
            row = [TILE_WALL]
            for x, char in enumerate(line):
                try:
                    tile = int(char)
                except ValueError:
                    tile = TILE_FLOOR

                row.append(tile)

                if tile in TILE_TO_EVENT_ID:
                    event_id = TILE_TO_EVENT_ID[tile]
                    grid_pos = (x + 1, y + 1)
                    if event_id not in self.event_positions:
                        self.event_positions[event_id] = []
                    self.event_positions[event_id].append(grid_pos)

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

    def get_event_positions(self, event_id: str) -> List[Tuple[int, int]]:
        return self.event_positions.get(event_id, [])

    def get_all_event_positions(self) -> Dict[str, List[Tuple[int, int]]]:
        return dict(self.event_positions)

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
