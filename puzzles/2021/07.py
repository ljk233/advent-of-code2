"""Advent of Code 2021 Day 7: The Treachery of Whales"""

import re
from math import ceil, floor
from statistics import mean, median

from advent_of_code import reader, tools

YEAR, DAY, TEST = 2021, 7, False


def solve():
    input_data = reader.read2(YEAR, DAY, test=TEST)
    initial_positions = parse_input_data(input_data)
    minimize_constant_fuel_cost(initial_positions)
    minimize_linear_fuel_cost(initial_positions)


@tools.solution(part=0)
def parse_input_data(input_data: str) -> list[int]:
    return [int(d) for d in re.findall(r"\d+", input_data)]


@tools.solution(part=1)
def minimize_constant_fuel_cost(initial_positions: list[int]) -> int:
    target = median(initial_positions)

    return int(sum(abs(d - target) for d in initial_positions))


@tools.solution(part=2)
def minimize_linear_fuel_cost(initial_positions: list[int]) -> int:
    real_target = mean(initial_positions)

    def cost(t):
        return sum(triangular(abs(d - t)) for d in initial_positions)

    return min(cost(floor(real_target)), cost(ceil(real_target)))


def triangular(num: int) -> int:
    return num * (num + 1) // 2


if __name__ == "__main__":
    solve()
