"""Advent of Code 2021 Day 12: Passage Pathing"""

import networkx as nx

from advent_of_code import reader, tools

YEAR, DAY, TEST = 2021, 12, False


def solve():
    input_data = reader.read_lines2(YEAR, DAY, test=TEST)
    cave_system = build_cave_system(input_data)
    count_paths(cave_system)
    count_revisiting_paths(cave_system)


@tools.solution(part=0)
def build_cave_system(input_data: list[str]) -> nx.Graph:
    return nx.Graph(line.split("-") for line in input_data)


@tools.solution(part=1)
def count_paths(caves: nx.Graph) -> int:
    return explore(caves)


@tools.solution(part=2)
def count_revisiting_paths(caves: nx.Graph) -> int:
    return explore(caves, can_revisit=True)


def explore(caves: nx.Graph, can_revisit: bool = False) -> int:
    stack = [("start", {"start"}, can_revisit)]
    path_count = 0

    while stack:
        cave, visited, can_revisit = stack.pop()

        if cave == "end":
            path_count += 1
            continue

        for nbr in caves.neighbors(cave):
            if nbr == "start":
                continue

            if nbr.isupper():
                stack.append((nbr, visited, can_revisit))
                continue

            if nbr not in visited:
                stack.append((nbr, visited | {nbr}, can_revisit))
                continue

            if can_revisit:
                stack.append((nbr, visited, False))

    return path_count


if __name__ == "__main__":
    solve()
