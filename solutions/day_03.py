from typing import List, Tuple
import re

mul_pattern = r"mul\((\d{1,3}),(\d{1,3})\)"


def get_valid_mul(input: List[str]) -> List[Tuple[int, int]]:
    # Find all valid mul operations and return the list of their two multiplicands
    # mul(2,3)xssmul(4,5) -> [(2, 3), (4, 5)]
    one_line_input = "".join(input)
    matches = re.findall(mul_pattern, one_line_input)
    return [(int(x), int(y)) for x, y in matches]


def get_valid_mul_do(input: List[str]) -> List[Tuple[int, int]]:
    # Find all valid mul operations after do() operation and return the list of their two multiplicands
    one_line_input = "".join(input)
    # Get only do()...don't() sections
    do_sections = one_line_input.split("do()")
    do_sections = [x.split("don't()", 1)[0] for x in do_sections]
    result: List[Tuple[int, int]] = []
    for section in do_sections:
        matches = re.findall(mul_pattern, section)
        result.extend(map(lambda x: (int(x[0]), int(x[1])), matches))
    return result


def solve_1(input: List[str]) -> str:
    valid_muls = get_valid_mul(input)
    return str(sum(x * y for x, y in valid_muls))


def solve_2(input: List[str]) -> str:
    valid_muls = get_valid_mul_do(input)
    return str(sum(x * y for x, y in valid_muls))
