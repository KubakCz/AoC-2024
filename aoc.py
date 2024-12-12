from typing import List, Iterable
import os
import argparse
import solutions.day_01
import solutions.day_02
import solutions.day_03
import solutions.day_04
import solutions.day_05
import solutions.day_06
import solutions.day_07
import solutions.day_08
import solutions.day_09
import solutions.day_10
import solutions.day_11
import solutions.day_12

solve_functions = [
    (solutions.day_01.solve_1, solutions.day_01.solve_2),
    (solutions.day_02.solve_1, solutions.day_02.solve_2),
    (solutions.day_03.solve_1, solutions.day_03.solve_2),
    (solutions.day_04.solve_1, solutions.day_04.solve_2),
    (solutions.day_05.solve_1, solutions.day_05.solve_2),
    (solutions.day_06.solve_1, solutions.day_06.solve_2),
    (solutions.day_07.solve_1, solutions.day_07.solve_2),
    (solutions.day_08.solve_1, solutions.day_08.solve_2),
    (solutions.day_09.solve_1, solutions.day_09.solve_2),
    (solutions.day_10.solve_1, solutions.day_10.solve_2),
    (solutions.day_11.solve_1, solutions.day_11.solve_2),
    (solutions.day_12.solve_1, solutions.day_12.solve_2),
]


def read_input(file: str) -> List[str]:
    with open(file) as f:
        return [line.strip() for line in f]


def get_input_files(day: int, include_samples: bool = False) -> List[str]:
    if not os.path.exists("inputs"):
        raise FileNotFoundError("The 'inputs' directory does not exist.")
    day_str = f"{day:02d}"
    files: Iterable[str] = filter(lambda x: day_str in x, os.listdir("inputs"))
    if not include_samples:
        # filter out the sample files
        files = filter(lambda x: "_e" not in x, files)
    else:
        # examples first
        examples = []
        not_examples = []
        for f in files:
            if "_e" in f:
                examples.append(f)
            else:
                not_examples.append(f)
        files = examples + not_examples
    return [f"inputs/{f}" for f in files]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int, help="The day of the challenge")
    parser.add_argument(
        "-e", "--examples", action="store_true", help="Include example input files"
    )
    args = parser.parse_args()

    # Check if the day is implemented
    if args.day < 1 or args.day > len(solve_functions):
        print("Day not implemented")
        exit(1)

    # Get the input files
    input_files = get_input_files(args.day, args.examples)
    if len(input_files) == 0:
        print("No input files found")
        exit(1)

    # Solve the challenges
    for file in input_files:
        print(f"--- Solution for {file} ---")
        input = read_input(file)
        solve = solve_functions[args.day - 1]
        solution_a = solve[0](input)
        print(f"Puzzle 1: {solution_a}")
        solution_b = solve[1](input)
        print(f"Puzzle 2: {solution_b}")
        print()
