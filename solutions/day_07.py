from math import ceil, log10
from typing import List, Tuple, Callable
import operator

Operation = Callable[[int, int], int]


def parse_line(line: str) -> Tuple[int, List[int]]:
    colon_index = line.index(":")
    test_value = int(line[:colon_index])
    components_part = line[colon_index + 2:]
    components = [int(num) for num in components_part.split(" ")]
    return test_value, components


def concatenate(a: int, b: int) -> int:
    return a * 10 ** ceil(log10(b)) + b


def test_equation_recursive(
        test_value: int,
        components: List[int],
        operators: List[Operation],
        starting_index: int,
        cumulative_result: int) -> bool:
    if len(components) == starting_index:
        return cumulative_result == test_value
    elif cumulative_result > test_value:
        return False  # No way of getting to the test_value
    for op in operators:
        if test_equation_recursive(
                test_value,
                components,
                operators,
                starting_index + 1,
                op(cumulative_result, components[starting_index])):
            return True
    return False


def test_equation(test_value: int, components: List[int], operators: List[Operation]) -> bool:
    # Strategy: Backtrack through the components, trying to find a way to the test_value
    return test_equation_recursive(test_value, components, operators, 1, components[0])


def solve(input: List[str], operators: List[Operation]) -> str:
    parsed_input = map(parse_line, input)
    possible_equations = filter(lambda x: test_equation(x[0], x[1], operators), parsed_input)
    calibration_result = map(lambda x: x[0], possible_equations)
    return f"Sum of the possible calibration results: {sum(calibration_result)}"


def solve_1(input: List[str]) -> str:
    return solve(input, [operator.add, operator.mul])


def solve_2(input: List[str]) -> str:
    return solve(input, [operator.add, operator.mul, concatenate])
