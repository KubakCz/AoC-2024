from typing import Dict, List, Tuple


def parse_input(input: List[str]) -> Tuple[List[int], List[int]]:
    l1 = []
    l2 = []
    for line in input:
        i = line.split("   ")
        l1.append(int(i[0]))
        l2.append(int(i[1]))
    return l1, l2


def list_to_counts(input_list: List[int]) -> Dict[int, int]:
    counts: Dict[int, int] = {}
    for i in input_list:
        if i in counts:
            counts[i] += 1
        else:
            counts[i] = 1
    return counts


def solve_1(input: List[str]) -> str:
    l1, l2 = parse_input(input)
    l1.sort()
    l2.sort()
    acc = sum(map(lambda line: abs(line[0] - line[1]), zip(l1, l2)))
    return str(acc)


def solve_2(input: List[str]) -> str:
    l1, l2 = parse_input(input)
    l1_counts = list_to_counts(l1)
    l2_counts = list_to_counts(l2)
    acc = 0
    for (value, count) in l1_counts.items():
        acc += value * count * l2_counts.get(value, 0)
    return str(acc)
