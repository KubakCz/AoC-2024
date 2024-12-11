from typing import Dict, List, Optional, Tuple
from math import log10


def parse_input(input: str) -> List[int]:
    return [int(num) for num in input.split(" ")]


def split_number(stone_number: int) -> Optional[Tuple[int, int]]:
    decimal_places = int(log10(stone_number)) + 1
    if decimal_places % 2 == 1:
        return None
    split = 10 ** (decimal_places // 2)
    return stone_number // split, stone_number % split


def get_stone_count(stone_number: int, depth: int, memo: Dict[Tuple[int, int], int]) -> int:
    # Strategy: Recursively calculate the number of stones at each depth. Use memoization to avoid recalculating.
    if (stone_number, depth) in memo:
        return memo[(stone_number, depth)]
    if depth <= 0:
        return 1

    if stone_number == 0:
        count = get_stone_count(2024, depth - 2, memo)  # Skip the stone 1
    else:
        split = split_number(stone_number)
        if split is None:
            count = get_stone_count(stone_number * 2024, depth - 1, memo)
        else:
            count = get_stone_count(split[0], depth - 1, memo) + get_stone_count(split[1], depth - 1, memo)
    memo[(stone_number, depth)] = count
    return count


def solve_1(input: List[str]) -> str:
    stones = parse_input(input[0])
    total = 0
    for stone in stones:
        total += get_stone_count(stone, 25, {})
    return f"Total number of stones: {total}"


def solve_2(input: List[str]) -> str:
    stones = parse_input(input[0])
    total = 0
    for stone in stones:
        total += get_stone_count(stone, 75, {})
    return f"Total number of stones: {total}"
