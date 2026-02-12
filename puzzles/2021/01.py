"""Advent of Code 2021 Day 1: Sonar Sweep"""

import itertools as it
from collections.abc import Iterable

from advent_of_code import reader, tools

YEAR, DAY = 2021, 1


def solve(test: bool = False):
    input_data = reader.read_lines2(YEAR, DAY, test)
    heights = process(input_data)
    count_successive_increasing(heights)
    count_aggregated_increasing(heights)


@tools.solution(part=0)
def process(input_data: list[str]) -> list[int]:
    return [int(line) for line in input_data]


@tools.solution(part=1)
def count_successive_increasing(heights: list[int]) -> int:
    return count_increasing(heights)


@tools.solution(part=2)
def count_aggregated_increasing(heights: list[int]) -> int:
    aggregated = (sum(win) for win in sliding_window(heights, 3))

    return count_increasing(aggregated)


def count_increasing(numbers: Iterable[int]) -> int:
    return sum(left <= right - 1 for left, right in it.pairwise(numbers))


def sliding_window[T](iterable: Iterable[T], n: int) -> Iterable[tuple[T, ...]]:
    data = [item for item in iterable]
    iters = (it.islice(data, i, None) for i in range(n))

    yield from zip(*iters)


if __name__ == "__main__":
    solve()
