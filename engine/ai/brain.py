import random
from typing import List, Tuple, Optional

from .context import Context
from .action import Action


class Brain:
    def __init__(self, top_n: int = 3, weights: List[float] = None):
        self.top_n = top_n
        self.weights = weights if weights is not None else [0.4, 0.4, 0.2]

    def decide(self, context: Context, actions: List[Action]) -> Tuple[Optional[Action], float]:
        utilities = []
        for action in actions:
            utility = action.calculate_utility(context)
            utilities.append((action, utility))

        utilities.sort(key=lambda x: x[1], reverse=True)

        top_candidates = utilities[:self.top_n]

        if not top_candidates:
            return None, 0.0

        selected = self._weighted_choice(top_candidates)
        return selected[0], selected[1]

    def _weighted_choice(self, items: List[Tuple]) -> Tuple:
        if len(items) == 1:
            return items[0]

        r = random.random()
        cumulative = 0.0
        effective_weights = self._normalize_weights(len(items))

        for i, item in enumerate(items):
            cumulative += effective_weights[i]
            if r <= cumulative:
                return item

        return items[-1]

    def _normalize_weights(self, num_items: int) -> List[float]:
        if num_items <= 0:
            return []

        if num_items >= len(self.weights):
            return self.weights[:num_items]

        weights_subset = self.weights[:num_items]
        total = sum(weights_subset)
        if total <= 0:
            return [1.0 / num_items] * num_items
        return [w / total for w in weights_subset]
