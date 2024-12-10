from typing import Dict, Generator, List, Set, Tuple


def get_antenas(input: List[str]) -> Dict[str, List[Tuple[int, int]]]:
    antenas: Dict[str, List[Tuple[int, int]]] = dict()
    for r, line in enumerate(input):
        for c, char in enumerate(line):
            if char != ".":
                if char not in antenas:
                    antenas[char] = []
                antenas[char].append((r, c))
    return antenas


def add_tuples(a1: Tuple[int, int], a2: Tuple[int, int]) -> Tuple[int, int]:
    return (a1[0] + a2[0], a1[1] + a2[1])


def sub_tuples(a1: Tuple[int, int], a2: Tuple[int, int]) -> Tuple[int, int]:
    return (a1[0] - a2[0], a1[1] - a2[1])


def generate_antinodes(antenas: List[Tuple[int, int]]) -> Generator[Tuple[int, int], None, None]:
    for i in range(len(antenas)):
        for j in range(i + 1, len(antenas)):
            diff = sub_tuples(antenas[j], antenas[i])
            yield add_tuples(antenas[j], diff)
            yield sub_tuples(antenas[i], diff)


def generate_resonant_antinodes(
        a1: Tuple[int, int],
        a2: Tuple[int, int],
        width: int,
        height: int) -> Generator[Tuple[int, int], None, None]:
    # First, yield the two antenas
    yield a1
    yield a2
    # Go in the direction of the vector a2 - a1
    diff = sub_tuples(a2, a1)
    pos = add_tuples(a2, diff)
    while 0 <= pos[0] < height and 0 <= pos[1] < width:
        yield pos
        pos = add_tuples(pos, diff)
    # Go in the direction of the vector a1 - a2
    pos = sub_tuples(a1, diff)
    while 0 <= pos[0] < height and 0 <= pos[1] < width:
        yield pos
        pos = sub_tuples(pos, diff)


def get_resonant_antinodes_for_cluster(antenas: List[Tuple[int, int]], width: int, height: int) -> Set[Tuple[int, int]]:
    antinodes: Set = set()
    for i in range(len(antenas)):
        for j in range(i + 1, len(antenas)):
            antinodes.update(generate_resonant_antinodes(antenas[i], antenas[j], width, height))
    return antinodes


def print_antinodes(antinodes: Set[Tuple[int, int]], width: int, height: int) -> None:
    for r in range(height):
        for c in range(width):
            if (r, c) in antinodes:
                print("#", end="")
            else:
                print(".", end="")
        print()


def solve_1(input: List[str]) -> str:
    antenas = get_antenas(input)
    width = len(input[0])
    height = len(input)
    antinodes: Set = set()
    for same_antenas in antenas.values():
        for antinode in generate_antinodes(same_antenas):
            if 0 <= antinode[0] < height and 0 <= antinode[1] < width:
                antinodes.add(antinode)
    return f"Antinodes in the grid: {len(antinodes)}"


def solve_2(input: List[str]) -> str:
    antenas = get_antenas(input)
    width = len(input[0])
    height = len(input)
    antinodes: Set = set()
    for same_antenas in antenas.values():
        antinodes.update(get_resonant_antinodes_for_cluster(same_antenas, width, height))
    return f"Antinodes in the grid: {len(antinodes)}"
