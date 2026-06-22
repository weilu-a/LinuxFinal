from abc import ABC, abstractmethod
from typing import Tuple, List

from .context import Context
from .consideration import Consideration


class Action(ABC):
    def __init__(self, action_id: str, consideration: Consideration):
        self.action_id = action_id
        self.consideration = consideration

    @abstractmethod
    def get_target_position(self, context: Context) -> Tuple[int, int]:
        pass

    @abstractmethod
    def get_duration(self) -> float:
        pass

    @abstractmethod
    def get_reward(self) -> float:
        pass

    def calculate_utility(self, context: Context) -> float:
        return self.consideration.evaluate(context)

    @abstractmethod
    def execute(self, context: Context):
        pass
