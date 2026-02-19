"""Advent of Code 2021 Day 3: Binary Diagnostic!"""

from collections import Counter
from collections.abc import Callable

from advent_of_code import grid_utils as gru
from advent_of_code import reader, tools

YEAR, DAY, TEST = 2021, 3, False


def solve():
    input_data = reader.read_lines2(YEAR, DAY, test=TEST)
    power_consumption(input_data)
    life_support_rating(input_data)


@tools.solution(part=1)
def power_consumption(diagnostic_ratings: list[list[str]]) -> int:
    transposed = gru.transpose(diagnostic_ratings)
    gamma = gamma_rating(transposed)
    epsilon = epsilon_rating(gamma)

    return int(gamma, 2) * int(epsilon, 2)


def gamma_rating(transposed: list[list[str]]) -> str:
    return "".join(most_common(Counter(col)) for col in transposed)


def epsilon_rating(gamma: str) -> str:
    return "".join("1" if b == "0" else "0" for b in gamma)


@tools.solution(part=2)
def life_support_rating(diagnostic_ratings: list[list[str]]) -> int:
    oxygen_generator = calculate_rating(diagnostic_ratings, lambda a, b: a == b)
    co2_scrubber = calculate_rating(diagnostic_ratings, lambda a, b: a != b)

    return int(oxygen_generator, 2) * int(co2_scrubber, 2)


def calculate_rating(diagnostic_ratings: list[list[str]], filter_fn: Callable) -> str:
    filtered = diagnostic_ratings[:]
    rating = ""
    columns = len(diagnostic_ratings[0]) - 1
    target_col = 0
    while target_col <= columns and len(filtered) >= 2:
        bit_count = Counter(line[target_col] for line in filtered)
        bit = most_common(bit_count)
        rating += bit
        filtered = [line for line in filtered if filter_fn(line[target_col], bit)]
        target_col += 1

    return "".join(filtered[-1])


def most_common(bit_count: Counter[str]) -> str:
    return "1" if bit_count["1"] >= bit_count["0"] else "0"


if __name__ == "__main__":
    solve()
