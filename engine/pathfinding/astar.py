import heapq
from dataclasses import dataclass
from typing import List, Tuple, Optional, Set, Dict


@dataclass(frozen=True, order=True)
class PriorityItem:
    priority: float
    position: Tuple[int, int]


class AStar:
    def __init__(self, grid_world):
        self.grid = grid_world
        self.width = grid_world.width
        self.height = grid_world.height

    def is_walkable(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return not self.grid.is_wall(x, y)

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = pos
        neighbors = []
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_walkable(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        if not self.is_walkable(end[0], end[1]):
            return []

        open_set: List[PriorityItem] = []
        heapq.heappush(open_set, PriorityItem(0.0, start))

        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g_score: Dict[Tuple[int, int], float] = {start: 0.0}
        f_score: Dict[Tuple[int, int], float] = {start: self.heuristic(start, end)}

        closed_set: Set[Tuple[int, int]] = set()

        while open_set:
            current = heapq.heappop(open_set).position

            if current == end:
                return self._reconstruct_path(came_from, current)

            closed_set.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor in closed_set:
                    continue

                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, end)
                    heapq.heappush(open_set, PriorityItem(f_score[neighbor], neighbor))

        return []

    def _reconstruct_path(self, came_from: Dict[Tuple[int, int], Tuple[int, int]],
                          current: Tuple[int, int]) -> List[Tuple[int, int]]:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path


def find_path(grid_world, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
    astar = AStar(grid_world)
    return astar.find_path(start, end)
