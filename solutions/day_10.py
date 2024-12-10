from collections import deque
from typing import List, Set, Tuple

Grid = List[List[int]]
ReachablePeaks = List[List[Set[Tuple[int, int]]]]


def input_to_grid(input: List[str]) -> Grid:
    return [[int(c) for c in line] for line in input]


def get_reachable_peaks(topo_map: Grid) -> ReachablePeaks:
    # Create a new grid which stores set of reachable peaks from each cell
    # Strategy: BFS starting from all peaks at once. Each peak has 1 reachable trailhead.
    reachable_peaks: ReachablePeaks = [[set() for c in range(len(topo_map[0]))] for _ in range(len(topo_map))]
    queue: deque[Tuple[int, int]] = deque()
    # Add all peaks to the queue
    for r in range(len(topo_map)):
        for c in range(len(topo_map[0])):
            if topo_map[r][c] == 9:
                queue.append((r, c))
                reachable_peaks[r][c].add((r, c))

    while queue:
        r, c = queue.popleft()
        height_to_update = topo_map[r][c] - 1
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(topo_map) and 0 <= nc < len(topo_map[0]) and topo_map[nr][nc] == height_to_update:
                # Found a cell, that can reach the current cell
                # => it can reach all peaks reachable from the current cell
                if height_to_update > 0 and len(reachable_peaks[nr][nc]) == 0:  # Not visited yet
                    queue.append((nr, nc))
                reachable_peaks[nr][nc].update(reachable_peaks[r][c])

    return reachable_peaks


def get_rating(topo_map: Grid) -> Grid:
    # Create a new grid which stores the rating of each cell
    # Strategy: Same as above, but we need to calculate the rating of each cell
    ratings = [[0] * len(topo_map[0]) for _ in range(len(topo_map))]
    queue: deque[Tuple[int, int]] = deque()
    # Add all peaks to the queue
    for r in range(len(topo_map)):
        for c in range(len(topo_map[0])):
            if topo_map[r][c] == 9:
                queue.append((r, c))
                ratings[r][c] = 1

    while queue:
        r, c = queue.popleft()
        height_to_update = topo_map[r][c] - 1
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(topo_map) and 0 <= nc < len(topo_map[0]) and topo_map[nr][nc] == height_to_update:
                # Found a cell, that can reach the current cell
                # => it can use all the tracks from the current cell
                if height_to_update > 0 and ratings[nr][nc] == 0:  # Not visited yet
                    queue.append((nr, nc))
                ratings[nr][nc] += ratings[r][c]

    return ratings


def solve_1(input: List[str]) -> str:
    topo_map = input_to_grid(input)
    reachable_peaks = get_reachable_peaks(topo_map)
    total_score = 0
    for r in range(len(topo_map)):
        for c in range(len(topo_map[0])):
            if topo_map[r][c] == 0:  # Trailhead
                total_score += len(reachable_peaks[r][c])
    return f"Sum of trailheads scores: {total_score}"


def solve_2(input: List[str]) -> str:
    topo_map = input_to_grid(input)
    ratings = get_rating(topo_map)
    total_score = 0
    for r in range(len(topo_map)):
        for c in range(len(topo_map[0])):
            if topo_map[r][c] == 0:  # Trailhead
                total_score += ratings[r][c]
    return f"Sum of trailheads scores: {total_score}"
