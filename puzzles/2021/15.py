"""Advent of Code 2021 Day 15: Chiton"""

import itertools as it

from advent_of_code import grid_utils as gru
from advent_of_code import reader, tools

YEAR, DAY, TEST = 2021, 15, False


def solve():
    input_data = reader.read_lines2(YEAR, DAY, test=TEST)
    navigate_cavern(input_data)
    navigate_actual_cavern(input_data)


@tools.solution(part=1)
def navigate_cavern(input_data: list[str]) -> int:
    cavern = scale_cavern(input_data, 1)
    r, c = gru.shape(input_data)

    def adj_fn(p: gru.Point):
        return [(nbr, cavern[nbr]) for nbr in p.get_neighbors(r, c)]

    target = gru.Point(r - 1, c - 1)
    dist, _ = gru.shortest_paths(gru.origin_point(), adj_fn, target=target)

    return dist[target]


@tools.solution(part=2)
def navigate_actual_cavern(input_data: list[str]) -> int:
    cavern = scale_cavern(input_data, 5)
    r, c = gru.shape(input_data)

    def adj_fn(p: gru.Point):
        return [(nbr, cavern[nbr]) for nbr in p.get_neighbors(5 * r, 5 * c)]

    target = gru.Point(5 * r - 1, 5 * c - 1)
    dist, _ = gru.shortest_paths(gru.origin_point(), adj_fn, target=target)

    return dist[target]


def scale_cavern(input_data: list[str], scale: int = 1) -> dict[gru.Point, int]:
    original_points = {p: int(val) for p, val in gru.generate_point_values(input_data)}
    rows, cols = gru.shape(input_data)

    full_cavern = {}
    for tile_i, tile_j in it.product(range(scale), range(scale)):
        for p, val in original_points.items():
            added_risk = tile_i + tile_j
            new_val = val + added_risk
            while new_val > 9:
                new_val -= 9

            new_point = gru.Point(p.i + (tile_i * rows), p.j + (tile_j * cols))
            full_cavern[new_point] = new_val

    return full_cavern


if __name__ == "__main__":
    solve()
