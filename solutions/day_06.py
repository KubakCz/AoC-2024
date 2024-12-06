from typing import List, Optional, Set, Tuple, Union

Grid = Union[List[List[str]], List[str]]


class Vector:
    def __init__(self, x: int, y: int):
        self.val = (x, y)

    def x(self) -> int:
        return self.val[0]

    def y(self) -> int:
        return self.val[1]

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.val[0] + other.val[0], self.val[1] + other.val[1])

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.val == other.val

    def __hash__(self) -> int:
        return hash(self.val)

    def __repr__(self) -> str:
        return f"({self.val[0]}, {self.val[1]})"


DIR_CYCLE = [Vector(0, -1), Vector(1, 0), Vector(0, 1), Vector(-1, 0)]


def starting_position(grid: Grid) -> Vector:
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "^":
                return Vector(c, r)
    raise ValueError("No starting position found")


def inbounds(pos: Vector, grid: Grid) -> bool:
    return 0 <= pos.x() < len(grid[0]) and 0 <= pos.y() < len(grid)


def next_position(pos: Vector, dir_index: int, grid: Grid) -> Tuple[Vector, int]:
    next_pos = pos + DIR_CYCLE[dir_index]
    while inbounds(next_pos, grid) and grid[next_pos.y()][next_pos.x()] == "#":
        # Turn right
        dir_index = (dir_index + 1) % 4
        next_pos = pos + DIR_CYCLE[dir_index]
    return next_pos, dir_index


def next_turning_point(pos: Vector, dir_index: int, grid: Grid) -> Optional[Tuple[Vector, int]]:
    # Returns (position of the next turn, direction after the turn) or None if no turn is found
    # Move forward while you can
    next_pos = pos + DIR_CYCLE[dir_index]
    while inbounds(next_pos, grid) and grid[next_pos.y()][next_pos.x()] != "#":
        pos = next_pos  # Pos will hold the last valid position
        next_pos = next_pos + DIR_CYCLE[dir_index]
    if not inbounds(next_pos, grid):
        return None
    # Turn
    dir_index = (dir_index + 1) % 4
    tmp_pos = pos + DIR_CYCLE[dir_index]
    while inbounds(tmp_pos, grid) and grid[tmp_pos.y()][tmp_pos.x()] == "#":
        dir_index = (dir_index + 1) % 4
        tmp_pos = pos + DIR_CYCLE[dir_index]
    return pos, dir_index


def find_cycle(
        starting_pos: Vector,
        starting_dir_index: int,
        grid: Grid,
        turning_points: Set[Tuple[Vector, int]]) -> bool:
    # Strategy: go until you find a repeating turning point => cycle
    turning_points = turning_points.copy()
    current_turning_point = next_turning_point(starting_pos, starting_dir_index, grid)
    while current_turning_point is not None and current_turning_point not in turning_points:
        turning_points.add(current_turning_point)
        current_turning_point = next_turning_point(*current_turning_point, grid)
    return current_turning_point is not None  # None => escaped the map, Not None => point repeated


def solve_1(input: List[str]) -> str:
    current_pos = starting_position(input)
    current_dir_index = 0
    visited: Set[Vector] = set()
    while inbounds(current_pos, input):
        visited.add(current_pos)
        current_pos, current_dir_index = next_position(current_pos, current_dir_index, input)
    return f"Visited locations {len(visited)}"


def solve_2(input: List[str]) -> str:
    # Strategy: Try placing obstacles infront of the current position and look for a cycle
    grid = [list(row) for row in input]  # List[List[str]] so we can modify individual characters
    current_pos = starting_position(grid)
    current_dir_index = 0
    cycle_counter = 0
    turning_points: Set[Tuple[Vector, int]] = set()  # (position of a turn, direction after the turn)
    while inbounds(current_pos, grid):
        # Mark the current position as visited (moving ignores it, but testing cycles won't build on it)
        grid[current_pos.y()][current_pos.x()] = "X"
        # Try placing obstacles infront of the current position and look for a cycle
        new_pos, new_dir_index = next_position(current_pos, current_dir_index, grid)
        if inbounds(new_pos, grid) and grid[new_pos.y()][new_pos.x()] == ".":
            grid[new_pos.y()][new_pos.x()] = "#"
            if find_cycle(current_pos, current_dir_index, grid, turning_points):
                cycle_counter += 1
            grid[new_pos.y()][new_pos.x()] = "."
        # Change in direction => turning point
        if new_dir_index != current_dir_index:
            turning_points.add((current_pos, new_dir_index))
            current_dir_index = new_dir_index
        # Move
        current_pos = new_pos
    return f"Number of cycles: {cycle_counter}"
