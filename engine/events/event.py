import json
import os
import random
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any
from enum import Enum

from engine.ai import Context, Action, AttributeConsideration, ConstantConsideration, EventState
from engine.grid_world import GridWorld


class DisplayStyle(Enum):
    MARKER = 'marker'
    TILE = 'tile'


@dataclass
class MarkerConfig:
    color: Tuple[int, int, int]
    label: str = ""


@dataclass
class TileConfig:
    tile_color: Tuple[int, int, int]
    label: str = ""


@dataclass
class DisplayConfig:
    style: DisplayStyle
    marker: Optional[MarkerConfig] = None
    tile: Optional[TileConfig] = None


@dataclass
class SingleLocation:
    grid_position: Tuple[int, int]


@dataclass
class ScoreConfig:
    base_score: float
    affected_by_state: bool
    target_attribute: str = ""


@dataclass
class ExecutionConfig:
    duration: float
    reward: float
    reward_attribute: str = ""


@dataclass
class EventConfig:
    id: str
    name: str
    type: str
    display: DisplayConfig
    locations: List[SingleLocation]
    score: ScoreConfig
    execution: ExecutionConfig
    has_multiple_locations: bool = False


class EventAction(Action):
    def __init__(self, config: EventConfig, grid_world: Optional[GridWorld] = None):
        self.config = config
        self._grid_world = grid_world

        if config.score.affected_by_state and config.score.target_attribute:
            consideration = AttributeConsideration(
                base_score=config.score.base_score,
                target_attribute=config.score.target_attribute,
                affected_by_state=True
            )
        else:
            consideration = ConstantConsideration(
                score=config.score.base_score
            )

        super().__init__(config.id, consideration)

    def set_grid_world(self, grid_world: GridWorld):
        self._grid_world = grid_world

    def _get_locations(self) -> List[Tuple[int, int]]:
        if self._grid_world:
            from_grid = self._grid_world.get_event_positions(self.config.id)
            if from_grid:
                return from_grid
        if self.config.locations:
            return [loc.grid_position for loc in self.config.locations]
        return []

    def get_random_target(self, current_pos: Tuple[int, int]) -> Tuple[int, int]:
        locations = self._get_locations()
        if not locations:
            return current_pos
        if len(locations) == 1:
            return locations[0]
        return random.choice(locations)

    def get_all_locations(self) -> List[Tuple[int, int]]:
        return self._get_locations()

    def get_target_position(self, context: Context) -> Tuple[int, int]:
        return self.get_random_target((0, 0))

    def get_duration(self) -> float:
        return self.config.execution.duration

    def get_reward(self) -> float:
        return self.config.execution.reward

    def get_reward_attribute(self) -> str:
        return self.config.execution.reward_attribute

    def get_display_style(self) -> DisplayStyle:
        return self.config.display.style

    def get_marker_color(self) -> Optional[Tuple[int, int, int]]:
        if self.config.display.marker:
            return self.config.display.marker.color
        return None

    def get_tile_color(self) -> Optional[Tuple[int, int, int]]:
        if self.config.display.tile:
            return self.config.display.tile.tile_color
        return None

    def get_label(self) -> str:
        if self.config.display.marker:
            return self.config.display.marker.label or ""
        if self.config.display.tile:
            return self.config.display.tile.label or ""
        return ""

    def execute(self, context: Context):
        target_pos = self.get_random_target(context.event_target_pos or (0, 0))
        context.current_event_id = self.config.id
        context.event_target_pos = target_pos
        context.event_duration = self.config.execution.duration
        context.event_reward = self.config.execution.reward
        context.event_reward_attribute = self.config.execution.reward_attribute
        context.event_base_score = self.config.score.base_score
        context.event_affected_by_state = self.config.score.affected_by_state

        display = self.config.display
        if display.style == DisplayStyle.MARKER and display.marker:
            context.event_marker_color = display.marker.color
        elif display.style == DisplayStyle.TILE and display.tile:
            context.event_marker_color = display.tile.tile_color


def load_event_config(filepath: str) -> EventConfig:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    display_data = data.get('display', {})
    display_style_str = display_data.get('style', 'marker')

    marker_config = None
    tile_config = None

    if display_style_str == 'marker':
        marker_data = display_data.get('marker', {})
        marker_config = MarkerConfig(
            color=tuple(marker_data.get('color', [255, 255, 255])),
            label=marker_data.get('label', '')
        )
    elif display_style_str == 'tile':
        tile_data = display_data.get('tile', {})
        tile_config = TileConfig(
            tile_color=tuple(tile_data.get('tile_color', [255, 255, 255])),
            label=tile_data.get('label', '')
        )

    display_config = DisplayConfig(
        style=DisplayStyle(display_style_str),
        marker=marker_config,
        tile=tile_config
    )

    locations = []
    if 'locations' in data:
        for loc_data in data['locations']:
            locations.append(SingleLocation(
                grid_position=tuple(loc_data['grid_position'])))
        has_multiple = len(locations) > 1
    elif 'location' in data:
        locations.append(SingleLocation(
            grid_position=tuple(data['location']['grid_position'])))
        has_multiple = False
    else:
        has_multiple = False

    score_data = data.get('score', {})
    score_config = ScoreConfig(
        base_score=score_data.get('base_score', 0.5),
        affected_by_state=score_data.get('affected_by_state', True),
        target_attribute=score_data.get('target_attribute', '')
    )

    exec_data = data.get('execution', {})
    execution_config = ExecutionConfig(
        duration=exec_data.get('duration', 2.0),
        reward=exec_data.get('reward', 0.0),
        reward_attribute=exec_data.get('reward_attribute', score_config.target_attribute)
    )

    return EventConfig(
        id=data['id'],
        name=data['name'],
        type=data.get('type', 'generic'),
        display=display_config,
        locations=locations,
        score=score_config,
        execution=execution_config,
        has_multiple_locations=has_multiple
    )


def load_all_events(directory: str) -> Dict[str, EventConfig]:
    events = {}

    if not os.path.exists(directory):
        return events

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            try:
                config = load_event_config(filepath)
                events[config.id] = config
            except Exception as e:
                print(f"Error loading event {filename}: {e}")

    return events


class EventManager:
    def __init__(self, grid_world: GridWorld, tile_size: int):
        self.grid_world = grid_world
        self.tile_size = tile_size
        self.event_configs: Dict[str, EventConfig] = {}
        self.event_actions: List[EventAction] = []

    def load_events(self, directory: str):
        self.event_configs = load_all_events(directory)
        self.event_actions = [
            EventAction(config, self.grid_world) for config in self.event_configs.values()
        ]

    def get_all_events(self) -> List[EventAction]:
        return self.event_actions

    def get_event_markers(self):
        markers = []
        for config in self.event_configs.values():
            display = config.display
            positions = self.grid_world.get_event_positions(config.id)

            if display.style == DisplayStyle.MARKER and display.marker:
                for pos in positions:
                    markers.append((
                        DisplayStyle.MARKER,
                        pos,
                        display.marker.color,
                        display.marker.label or ""
                    ))
            elif display.style == DisplayStyle.TILE and display.tile:
                for pos in positions:
                    markers.append((
                        DisplayStyle.TILE,
                        pos,
                        display.tile.tile_color,
                        display.tile.label or ""
                    ))
        return markers

    def start_event(self, action: EventAction, context: Context):
        action.execute(context)
        context.event_state = EventState.PATHFIND

    def update_executing(self, context: Context, delta_time: float) -> bool:
        if context.event_state != EventState.EXECUTING:
            return False

        context.event_remaining_time -= delta_time

        if context.event_remaining_time <= 0:
            if context.event_reward != 0 and context.event_reward_attribute:
                attr = context.get_attribute(context.event_reward_attribute)
                if attr:
                    attr.apply_reward(context.event_reward)
            context.event_state = EventState.IDLE
            context.current_event_id = None
            return True

        return False

    def is_event_completed(self, context: Context) -> bool:
        return context.event_state == EventState.IDLE and context.current_event_id is None
