from abc import ABC, abstractmethod
from typing import Tuple

from .context import Context


class Consideration(ABC):
    def __init__(self, base_score: float = 1.0, affected_by_state: bool = True):
        self.base_score = base_score
        self.affected_by_state = affected_by_state

    @abstractmethod
    def evaluate(self, context: Context) -> float:
        pass


class AttributeConsideration(Consideration):
    def __init__(self, base_score: float, target_attribute: str, affected_by_state: bool = True):
        super().__init__(base_score, affected_by_state)
        self.target_attribute = target_attribute

    def evaluate(self, context: Context) -> float:
        if not self.affected_by_state:
            return max(0.0, min(1.0, self.base_score))

        attr = context.get_attribute(self.target_attribute)
        if not attr:
            return max(0.0, min(1.0, self.base_score))

        t = (-attr.value + attr.max) / (attr.max - attr.min) if attr.max != attr.min else 0.5
        t = max(0.0, min(1.0, t))

        if attr.utility_type == 'linear':
            utility = t
        else:
            utility = t ** attr.k

        final_score = utility * self.base_score
        return max(0.0, min(1.0, final_score))


class ConstantConsideration(Consideration):
    def __init__(self, score: float = 0.5):
        super().__init__(score, affected_by_state=False)

    def evaluate(self, context: Context) -> float:
        return max(0.0, min(1.0, self.base_score))
