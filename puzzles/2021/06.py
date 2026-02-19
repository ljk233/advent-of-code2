"""Advent of Code 2021 Day 6: Lanternfish"""

import re
from collections import Counter

from advent_of_code import reader, tools

YEAR, DAY, TEST = 2021, 6, False


def solve():
    input_data = reader.read2(YEAR, DAY, test=TEST)
    inital_state = parse_input_data(input_data)
    simulate_80(inital_state)
    simulate_256(inital_state)


@tools.solution(part=0)
def parse_input_data(input_data: str) -> Counter[int]:
    return Counter(int(d) for d in re.findall(r"\d+", input_data))


@tools.solution(part=1)
def simulate_80(initial_state: Counter[int]) -> int:
    return simulate_many(initial_state, 80).total()


@tools.solution(part=2)
def simulate_256(initial_state: Counter[int]) -> int:
    return simulate_many(initial_state, 256).total()


def simulate_many(state: Counter[int], days: int) -> Counter[int]:
    for _ in range(days):
        state = simulate(state)

    return state


def simulate(state: Counter[int]) -> Counter[int]:
    new_counter = Counter({decrease(day): k for day, k in state.items()})
    new_counter[6] += new_counter[8]

    return new_counter


def decrease(day: int) -> int:
    return day - 1 if day >= 1 else 8


if __name__ == "__main__":
    solve()
