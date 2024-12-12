from typing import Callable, Dict, List
from .unionfind import UnionFind


class Region:
    def __init__(self) -> None:
        self.area = 0
        self.perimeter = 0

    def get_price(self) -> int:
        return self.area * self.perimeter


def get_borders(r: int, c: int, region_grid: List[List[int]]) -> int:
    borders = 0
    if r == 0 or region_grid[r][c] != region_grid[r - 1][c]:
        borders += 1
    if r == len(region_grid) - 1 or region_grid[r][c] != region_grid[r + 1][c]:
        borders += 1
    if c == 0 or region_grid[r][c] != region_grid[r][c - 1]:
        borders += 1
    if c == len(region_grid[0]) - 1 or region_grid[r][c] != region_grid[r][c + 1]:
        borders += 1
    return borders


def get_border_starts(r: int, c: int, region_grid: List[List[int]]) -> int:
    starts = 0
    if r == 0 or region_grid[r][c] != region_grid[r - 1][c]:
        # Has border on top
        # => start of a new border if
        # - first column
        # - different from the left cell
        # - same as the left cell and the left cell in the previous row
        if c == 0  \
                or region_grid[r][c] != region_grid[r][c - 1] \
                or (r != 0 and region_grid[r][c - 1] == region_grid[r - 1][c - 1]):
            starts += 1
    if r == len(region_grid) - 1 or region_grid[r][c] != region_grid[r + 1][c]:
        # Has border on bottom
        # => start of a new border if
        # - first column
        # - different from the left cell
        # - same as the left cell and the left cell in the next row
        if c == 0  \
                or region_grid[r][c] != region_grid[r][c - 1] \
                or (r != len(region_grid) - 1 and region_grid[r][c - 1] == region_grid[r + 1][c - 1]):
            starts += 1
    if c == 0 or region_grid[r][c] != region_grid[r][c - 1]:
        # Has border on left
        # => start of a new border if
        # - first row
        # - different from the top cell
        # - same as the top cell and the top cell in the previous column
        if r == 0  \
                or region_grid[r][c] != region_grid[r - 1][c] \
                or (c != 0 and region_grid[r - 1][c] == region_grid[r - 1][c - 1]):
            starts += 1
    if c == len(region_grid[0]) - 1 or region_grid[r][c] != region_grid[r][c + 1]:
        # Has border on right
        # => start of a new border if
        # - first row
        # - different from the top cell
        # - same as the top cell and the top cell in the next column
        if r == 0  \
                or region_grid[r][c] != region_grid[r - 1][c] \
                or (c != len(region_grid[0]) - 1 and region_grid[r - 1][c] == region_grid[r - 1][c + 1]):
            starts += 1
    return starts


def mark_regions(input: List[str]) -> List[List[int]]:
    # Two-pass algorithm for marking connected components
    region_grid: List[List[int]] = [[0] * len(input[0]) for _ in range(len(input))]
    equivalent_regions = UnionFind()
    region_id = 1

    # Mark the first row
    region_grid[0][0] = region_id
    equivalent_regions.add(region_id)
    for c in range(1, len(input[0])):
        if input[0][c] != input[0][c - 1]:
            region_id += 1
            equivalent_regions.add(region_id)
        region_grid[0][c] = region_id

    # Mark the rest of the grid
    for r in range(1, len(input)):
        if input[r][0] != input[r - 1][0]:
            region_id += 1
            equivalent_regions.add(region_id)
            region_grid[r][0] = region_id
        else:
            region_grid[r][0] = region_grid[r - 1][0]
        for c in range(1, len(input[0])):
            if input[r][c] == input[r - 1][c] and input[r][c] == input[r][c - 1]:
                # Found one region with two different ids
                region_grid[r][c] = min(region_grid[r - 1][c], region_grid[r][c - 1])
                equivalent_regions.union(region_grid[r - 1][c], region_grid[r][c - 1])
            elif input[r][c] == input[r - 1][c]:
                region_grid[r][c] = region_grid[r - 1][c]
            elif input[r][c] == input[r][c - 1]:
                region_grid[r][c] = region_grid[r][c - 1]
            else:
                # New region
                region_id += 1
                equivalent_regions.add(region_id)
                region_grid[r][c] = region_id

    # Update the equivalent regions
    for r in range(len(input)):
        for c in range(len(input[0])):
            region_grid[r][c] = equivalent_regions.find(region_grid[r][c])

    return region_grid


def solve(input: List[str], perimeter_function: Callable[[int, int, List[List[int]]], int]) -> str:
    region_grid = mark_regions(input)
    regions: Dict[int, Region] = dict()
    for r in range(len(region_grid)):
        for c in range(len(region_grid[0])):
            region = regions.setdefault(region_grid[r][c], Region())
            region.area += 1
            region.perimeter += perimeter_function(r, c, region_grid)

    prices = map(lambda region: region.get_price(), regions.values())
    return f"Total price: {sum(prices)}"


def solve_1(input: List[str]) -> str:
    return solve(input, get_borders)


def solve_2(input: List[str]) -> str:
    return solve(input, get_border_starts)
