import json
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class NPCConfig:
    id: str
    name: str
    start_position: Tuple[int, int]
    initial_state_score: float
    decay_interval: float
    decay_amount: float
    decay_min: float
    decay_max: float
    utility_k: float
    movement_speed: float


class NPC:
    def __init__(self, config: NPCConfig, tile_size: int):
        self.config = config
        self.tile_size = tile_size

        self.state_score: float = config.initial_state_score
        self.grid_position: Tuple[int, int] = config.start_position
        self.pixel_position: Tuple[float, float] = (
            config.start_position[0] * tile_size + tile_size / 2,
            config.start_position[1] * tile_size + tile_size / 2
        )

        self.path: List[Tuple[int, int]] = []
        self.path_index: int = 0
        self.moving: bool = False
        self.movement_speed: float = config.movement_speed

    @classmethod
    def load_from_json(cls, filepath: str, tile_size: int) -> 'NPC':
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        start_position = tuple(data['initial_state']['start_position'])
        movement_speed = data['movement']['speed']

        if 'attributes' in data:
            first_attr_name = list(data['attributes'].keys())[0]
            first_attr = data['attributes'][first_attr_name]
            initial_state_score = first_attr.get('initial_value', 0.0)
            decay_interval = first_attr.get('decay_interval', 5.0)
            decay_amount = first_attr.get('decay_amount', -1.0)
            decay_min = first_attr.get('min', -10.0)
            decay_max = first_attr.get('max', 10.0)
            utility_k = first_attr.get('k', 2.0)
        else:
            initial_state_score = data['initial_state'].get('state_score', 0.0)
            decay_interval = data['decay']['interval']
            decay_amount = data['decay']['amount']
            decay_min = data['decay']['min']
            decay_max = data['decay']['max']
            utility_k = data['utility']['k']

        config = NPCConfig(
            id=data['id'],
            name=data['name'],
            start_position=start_position,
            initial_state_score=initial_state_score,
            decay_interval=decay_interval,
            decay_amount=decay_amount,
            decay_min=decay_min,
            decay_max=decay_max,
            utility_k=utility_k,
            movement_speed=movement_speed
        )

        return cls(config, tile_size)

    def set_path(self, path: List[Tuple[int, int]]):
        self.path = path
        self.path_index = 0
        self.moving = len(path) > 0

    def stop_moving(self):
        self.moving = False
        self.path = []
        self.path_index = 0

    def update_position(self, delta_time: float) -> bool:
        if not self.moving or not self.path:
            return False

        if self.path_index >= len(self.path):
            self.stop_moving()
            return True

        target_grid = self.path[self.path_index]
        target_pixel = (
            target_grid[0] * self.tile_size + self.tile_size / 2,
            target_grid[1] * self.tile_size + self.tile_size / 2
        )

        dx = target_pixel[0] - self.pixel_position[0]
        dy = target_pixel[1] - self.pixel_position[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5

        move_distance = self.movement_speed * self.tile_size * delta_time

        if distance <= move_distance:
            self.pixel_position = target_pixel
            self.grid_position = target_grid
            self.path_index += 1

            if self.path_index >= len(self.path):
                self.stop_moving()
                return True
        else:
            if distance > 0:
                dir_x = dx / distance
                dir_y = dy / distance

                if abs(dir_x) > abs(dir_y):
                    new_x = self.pixel_position[0] + dir_x * move_distance
                    new_y = target_pixel[1]
                else:
                    new_x = target_pixel[0]
                    new_y = self.pixel_position[1] + dir_y * move_distance

                self.pixel_position = (new_x, new_y)

        return False

    def is_at_target(self, target: Tuple[int, int]) -> bool:
        return self.grid_position == target

    def has_reached_path_end(self) -> bool:
        return not self.moving and self.path_index > 0

    def get_pixel_center(self) -> Tuple[float, float]:
        return self.pixel_position

    def get_grid_position(self) -> Tuple[int, int]:
        return self.grid_position
