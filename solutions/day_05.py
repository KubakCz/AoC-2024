from typing import List, Dict, Set


class ParsedInput:
    def __init__(self, input: List[str]):
        line_iter = iter(input)

        # key: page number, value: set of pages, that need to be after the key
        # e.g. 1: {2, 3} means that pages 2 and 3 need to be after page 1
        self.rules: Dict[int, Set[int]] = dict()
        for line in line_iter:
            if line == "":  # read rules until empty line
                break
            a = int(line[0:2])
            b = int(line[3:5])
            rule_set = self.rules.get(a)
            if rule_set is None:
                rule_set = {b}
                self.rules[a] = rule_set
            else:
                rule_set.add(b)

        # list of updates - of list of pages
        self.updates: List[List[int]] = []
        for line in line_iter:  # read rest of the input
            update = [int(x) for x in line.split(",")]
            assert len(update) % 2 == 1  # odd number of pages
            self.updates.append(update)


def update_ordered(update: List[int], rules: Dict[int, Set[int]]) -> bool:
    # Returns True if the update is correctly ordered according to the rules
    previous_pages = {update[0]}
    for i in range(1, len(update)):
        page = update[i]
        page_rules = rules.get(page, set())
        if page_rules.intersection(previous_pages):
            # some pages that need to be after this page are before it
            return False
        previous_pages.add(page)
    return True


def filter_rules(rules: Dict[int, Set[int]], update: List[int]) -> Dict[int, Set[int]]:
    # Keep only the rules that are relevant for the update
    relevant_rules = {}
    for page in update:
        page_rules = rules.get(page, set())
        relevant_rules[page] = page_rules.intersection(update)
    return relevant_rules


def sort_update(update: List[int], rules: Dict[int, Set[int]]) -> List[int]:
    filtered_rules = filter_rules(rules, update)
    # Rule set contains all the pages that need to be after the page => sort by the number of rules
    # If there would be "transitive" rules ({10|20, 20|30}), this would not work
    sorted_update = sorted(update, key=lambda x: len(filtered_rules[x]), reverse=True)
    # for i, page in enumerate(sorted_update):
    #     assert len(filtered_rules[page]) == len(update) - i - 1, str(update)
    return sorted_update


def get_middle_page(update: List[int]) -> int:
    return update[len(update) // 2]


def solve_1(input: List[str]) -> str:
    parsed = ParsedInput(input)
    ordered_updates = filter(lambda x: update_ordered(x, parsed.rules), parsed.updates)
    middle_pages = map(get_middle_page, ordered_updates)
    return f"Sum of middle pages: {sum(middle_pages)}"


def solve_2(input: List[str]) -> str:
    parsed = ParsedInput(input)
    unordered_updates = filter(lambda x: not update_ordered(x, parsed.rules), parsed.updates)
    sorted_updates = map(lambda x: sort_update(x, parsed.rules), unordered_updates)
    middle_pages = map(get_middle_page, sorted_updates)
    return f"Sum of middle pages: {sum(middle_pages)}"
