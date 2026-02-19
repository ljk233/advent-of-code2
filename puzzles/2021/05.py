"""Advent of Code 2021 Day 5: Hydrothermal Venture"""

import itertools as it
import re
from collections import Counter

from advent_of_code import grid_utils as gru
from advent_of_code import reader, tools

YEAR, DAY, TEST = 2021, 5, False


def solve():
    input_data = reader.read_lines2(YEAR, DAY, test=TEST)
    lines = parse_input_data(input_data)
    count_orthogonal_overlaps(lines)
    count_all_overlaps(lines)


@tools.solution(part=0)
def parse_input_data(input_data: list[str]) -> list[list[gru.Point]]:
    lines = []
    for line in input_data:
        a, b, c, d = [int(d) for d in re.findall(r"\d+", line)]
        lines.append(collect_line(gru.Point(a, b), gru.Point(c, d)))

    return lines


@tools.solution(part=1)
def count_orthogonal_overlaps(lines: list[list[gru.Point]]) -> int:
    orthog_lines = [line for line in lines if 0 in get_unit_delta(line[0], line[-1])]

    return count_overlapping_points(orthog_lines)


@tools.solution(part=2)
def count_all_overlaps(lines: list[list[gru.Point]]) -> int:
    return count_overlapping_points(lines)


def count_overlapping_points(lines: list[list[gru.Point]]) -> int:
    counter = Counter(p for p in it.chain(*lines))

    return sum(1 for k in counter.values() if k >= 2)


def collect_line(p1: gru.Point, p2: gru.Point) -> list[gru.Point]:
    unit_delta = get_unit_delta(p1, p2)
    line = [p1]
    while line[-1] != p2:
        p = line[-1] + unit_delta
        line.append(p)

    return line


def get_unit_delta(p1: gru.Point, p2: gru.Point) -> gru.Point:
    di = get_unit_change(p1.i, p2.i)
    dj = get_unit_change(p1.j, p2.j)

    return gru.Point(di, dj)


def get_unit_change(a: int, b: int) -> int:
    if a == b:
        return 0

    return (b - a) // abs(b - a)


if __name__ == "__main__":
    solve()
