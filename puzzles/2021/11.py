"""Advent of Code 2021 Day 11: Dumbo Octopus"""

import functools
from collections import Counter

from advent_of_code import grid_utils as gru
from advent_of_code import reader, tools

Octopuses = Counter[gru.Point]
ShapeLike = tuple[int, int]


YEAR, DAY, TEST = 2021, 11, False
THRESHOLD = 10


def solve():
    input_data = reader.read_lines2(YEAR, DAY, test=TEST)
    count_100_ticks(input_data)
    find_tick_all_flashing(input_data)


@tools.solution(part=1)
def count_100_ticks(input_data: list[str]) -> int:
    state, shape = map_initial_state(input_data)
    flashes = 0
    for _ in range(100):
        state, flashed = tick(state, shape)
        flashes += flashed

    return flashes


@tools.solution(part=2)
def find_tick_all_flashing(input_data: list[str], max_ticks: int = 1_000) -> int:
    state, shape = map_initial_state(input_data)
    for k in range(1, max_ticks):
        state, flashed = tick(state, shape)
        if flashed == len(state):
            return k

    return -1


def map_initial_state(input_data: list[str]) -> tuple[Octopuses, ShapeLike]:
    state = Counter({p: int(val) for p, val in gru.generate_point_values(input_data)})
    shape = gru.shape(input_data)

    return state, shape


def tick(state: Octopuses, shape: ShapeLike) -> tuple[Octopuses, int]:
    next_state = Counter(state)
    next_state.update(n for n in state)
    flashing = [n for n, val in next_state.items() if val >= THRESHOLD]
    flashed = set()
    while flashing:
        n = flashing.pop()
        if next_state[n] < THRESHOLD:
            continue

        if n in flashed:
            continue

        flashed.add(n)
        neighbors = get_neighbors(n, shape)
        next_state.update(neighbors)
        flashing.extend(neighbors)

    for n in flashed:
        next_state[n] = 0

    return next_state, len(flashed)


@functools.cache
def get_neighbors(point: gru.Point, shape: ShapeLike) -> list[gru.Point]:
    return [neighbor for neighbor in point.get_neighbors(*shape, diagonals=True)]


if __name__ == "__main__":
    solve()
