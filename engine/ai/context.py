from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict
from enum import Enum


class EventState(Enum):
    IDLE = 'idle'
    PATHFIND = 'pathfinding'
    EXECUTING = 'executing'


@dataclass
class AttributeData:
    value: float
    min: float
    max: float
    decay_interval: float
    decay_amount: float
    decay_stop_at_min: bool
    utility_type: str
    k: float
    last_decay_time: float = 0.0

    def clamp(self):
        self.value = max(self.min, min(self.max, self.value))

    def apply_reward(self, reward: float):
        self.value += reward
        self.clamp()

    def update_decay(self, current_time: float) -> bool:
        if self.decay_stop_at_min and self.value <= self.min:
            return False

        if current_time - self.last_decay_time >= self.decay_interval:
            new_value = self.value + self.decay_amount

            if self.decay_stop_at_min and new_value < self.min:
                self.value = self.min
            else:
                self.value = new_value
                self.clamp()

            self.last_decay_time = current_time
            return True

        return False


@dataclass
class Context:
    attributes: Dict[str, AttributeData]

    event_state: EventState = EventState.IDLE
    current_event_id: Optional[str] = None
    event_target_pos: Optional[Tuple[int, int]] = None
    event_duration: float = 0.0
    event_remaining_time: float = 0.0
    event_reward: float = 0.0
    event_reward_attribute: Optional[str] = None
    event_base_score: float = 0.0
    event_affected_by_state: bool = False
    event_marker_color: Optional[Tuple[int, int, int]] = None

    path: List[Tuple[int, int]] = field(default_factory=list)
    path_index: int = 0

    def __post_init__(self):
        if self.path is None:
            self.path = []

    def get_attribute(self, attr_name: str) -> Optional[AttributeData]:
        return self.attributes.get(attr_name)

    def update_all_decay(self, current_time: float) -> Dict[str, bool]:
        results = {}
        for attr_name, attr_data in self.attributes.items():
            results[attr_name] = attr_data.update_decay(current_time)
        return results
