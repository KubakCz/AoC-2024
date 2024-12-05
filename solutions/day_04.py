from typing import List

MS_ORD = ord("M") + ord("S")


def horizontal_fit(r: int, c: int, input: List[str]) -> bool:
    return c + 3 < len(input[r])


def vertical_fit(r: int, c: int, input: List[str]) -> bool:
    return r + 3 < len(input)


def horizontal(r: int, c: int, input: List[str]) -> bool:
    return input[r][c + 1] == "M" and input[r][c + 2] == "A" and input[r][c + 3] == "S"


def horizontal_reverse(r: int, c: int, input: List[str]) -> bool:
    return input[r][c + 1] == "A" and input[r][c + 2] == "M" and input[r][c + 3] == "X"


def vertical(r: int, c: int, input: List[str]) -> bool:
    return input[r + 1][c] == "M" and input[r + 2][c] == "A" and input[r + 3][c] == "S"


def vertical_reverse(r: int, c: int, input: List[str]) -> bool:
    return input[r + 1][c] == "A" and input[r + 2][c] == "M" and input[r + 3][c] == "X"


def diagonal_r(r: int, c: int, input: List[str]) -> bool:
    return input[r + 1][c + 1] == "M" and input[r + 2][c + 2] == "A" and input[r + 3][c + 3] == "S"


def diagonal_r_reverse(r: int, c: int, input: List[str]) -> bool:
    return input[r + 1][c + 1] == "A" and input[r + 2][c + 2] == "M" and input[r + 3][c + 3] == "X"


def diagonal_l(r: int, c: int, input: List[str]) -> bool:
    return input[r + 1][c - 1] == "M" and input[r + 2][c - 2] == "A" and input[r + 3][c - 3] == "S"


def diagonal_l_reverse(r: int, c: int, input: List[str]) -> bool:
    return input[r + 1][c - 1] == "A" and input[r + 2][c - 2] == "M" and input[r + 3][c - 3] == "X"


def x_mas(r: int, c: int, input: List[str]) -> bool:
    return ord(input[r - 1][c - 1]) + ord(input[r + 1][c + 1]) == MS_ORD \
        and ord(input[r - 1][c + 1]) + ord(input[r + 1][c - 1]) == MS_ORD


def solve_1(input: List[str]) -> str:
    # Find all XMAS
    # Strategy: Find either X or M, check to right, down, right-down, left-down
    height = len(input)
    width = len(input[0])
    counter = 0
    for r in range(height):
        for c in range(width):
            if input[r][c] == "X":
                fit_h = horizontal_fit(r, c, input)
                fit_v = vertical_fit(r, c, input)
                if fit_h and horizontal(r, c, input):
                    # print("Xh", r, c)
                    counter += 1
                if fit_v and vertical(r, c, input):
                    # print("Xv", r, c)
                    counter += 1
                if fit_h and fit_v and diagonal_r(r, c, input):
                    # print("Xdr", r, c)
                    counter += 1
                if fit_v and c >= 3 and diagonal_l(r, c, input):
                    # print("Xdl", r, c)
                    counter += 1
            elif input[r][c] == "S":
                fit_h = horizontal_fit(r, c, input)
                fit_v = vertical_fit(r, c, input)
                if fit_h and horizontal_reverse(r, c, input):
                    # print("Sh", r, c)
                    counter += 1
                if fit_v and vertical_reverse(r, c, input):
                    # print("Sv", r, c)
                    counter += 1
                if fit_h and fit_v and diagonal_r_reverse(r, c, input):
                    # print("Sdr", r, c)
                    counter += 1
                if fit_v and c >= 3 and diagonal_l_reverse(r, c, input):
                    # print("Sdl", r, c)
                    counter += 1
    return str(counter)


def solve_2(input: List[str]) -> str:
    # Find all X-MAS
    # Strategy: Find A, check diagonals
    height = len(input)
    width = len(input[0])
    counter = 0
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            if input[r][c] == "A" and x_mas(r, c, input):
                counter += 1
    return str(counter)
