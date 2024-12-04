from typing import  Generator, List


def parse_report(report: str) -> List[int]:
    # "1 2 3 4 5" -> [1, 2, 3, 4, 5]
    return [int(x) for x in report.split(" ")]


def safe_steps(report: List[int]) -> Generator[bool, None, None]:
    pn = report[0]
    diff = 0
    for i in range(1, len(report)):
        n = report[i]
        new_diff = n - pn
        yield diff * new_diff >= 0 and 0 < abs(new_diff) < 4
        diff = new_diff
        pn = n


def is_safe(report: List[int]) -> bool:
    return all(safe_steps(report))


def skip_level(report: List[int]) -> List[List[int]]:
    # 1 2 3 4 -> [[2, 3, 4], [1, 3, 4], [1, 2, 4], [1, 2, 3]]
    return [report[:i] + report[i + 1:] for i in range(len(report))]


def inefficient_is_nearly_safe(report: List[int]) -> bool:
    # Very inefficient, but works. I may return to this later...
    return any(is_safe(skipped) for skipped in skip_level(report))

# This is big mess, which is not working properly
# def is_nearly_safe(report: List[int]) -> bool:
#     # Safe with skipping one level at most
#     if len(report) == 2:  # only two levels => can skip one
#         return True

#     skipped = False

#     # first step
#     pn = report[0]
#     n = report[1]
#     diff = n - pn

#     # first step is too big
#     if not (0 < abs(diff) < 4):
#         skipped = True
#         # try skipping n
#         diff = report[2] - pn
#         if not (0 < abs(diff) < 4):
#             # try skipping pn
#             pn = report[1]
#             diff = report[2] - report[1]
#             if not (0 < abs(diff) < 4):  # skipping doesn't help
#                 if inefficient_is_nearly_safe(report):
#                     print(report)
#                 return False
#     elif diff * (report[2] - n) < 0:  # step in opposite direction
#         if len(report) == 3:
#             return True  # can skip last level
#         if diff * (report[3] - n) < 0:
#             # skip report[0]
#             skipped = True
#             pn = n
#             diff = report[2] - n
#         # else not skipping, skip next step
#     else:
#         pn = n

#     for i in range(2, len(report)):
#         n = report[i]
#         new_diff = n - pn
#         if diff * new_diff < 0:  # step in opposite direction
#             if skipped:
#                 if inefficient_is_nearly_safe(report):
#                     print(report)
#                 return False
#             skipped = True
#             # try skipping n
#             if i + 1 == len(report):  # no next step => can skip
#                 continue
#             # diff stays the same
#             new_diff = report[i + 1] - pn
#             if diff * new_diff > 0 and 0 < abs(new_diff) < 4:
#                 continue
#             # try skipping pn
#             diff = n - report[i - 2]
#             new_diff = report[i + 1] - n
#             if diff * new_diff > 0 and 0 < abs(diff) < 4 and 0 < abs(new_diff) < 4:
#                 pn = n
#                 continue
#             # skipping doesn't help
#             return False
#         elif not (0 < abs(new_diff) < 4):  # too big step => need to skip n
#             if skipped:
#                 if inefficient_is_nearly_safe(report):
#                     print(report)
#                 return False
#             skipped = True
#         else:  # safe step
#             diff = new_diff
#             pn = n
#     return True


def solve_1(input: List[str]) -> str:
    reports = [parse_report(report) for report in input]
    safe_reports = [report for report in reports if is_safe(report)]
    return f"Safe: {len(safe_reports)} | Unsafe: {len(reports) - len(safe_reports)}"


def solve_2(input: List[str]) -> str:
    reports = [parse_report(report) for report in input]
    nearly_safe_reports = [report for report in reports if inefficient_is_nearly_safe(report)]
    return f"Nearly safe: {len(nearly_safe_reports)} | Unsafe: {len(reports) - len(nearly_safe_reports)}"
