"""Advent of Code 2021 Day 9: Smoke Basin"""

from math import prod

import networkx as nx

from advent_of_code import grid_utils as gru
from advent_of_code import reader, tools

YEAR, DAY, TEST = 2021, 9, False


def solve():
    input_data = reader.read_lines2(YEAR, DAY, test=TEST)
    height_map = build_graph(input_data)
    risk_level(height_map)
    find_largest_three_basins(height_map)


@tools.solution(part=0)
def build_graph(input_data: list[str]) -> nx.DiGraph:
    digraph = nx.DiGraph()
    node_generator = gru.generate_point_values(input_data)
    for p, val in node_generator:
        if val == "9":
            continue

        digraph.add_node(p, height=int(val))

    for u, v in gru.generate_edges(input_data):
        if not all(n in digraph for n in (u, v)):
            continue

        if digraph.nodes[u]["height"] > digraph.nodes[v]["height"]:
            digraph.add_edge(u, v)

        if digraph.nodes[v]["height"] > digraph.nodes[u]["height"]:
            digraph.add_edge(v, u)

    return digraph


@tools.solution(part=1)
def risk_level(height_map: nx.DiGraph) -> int:
    risk = 0
    for u, out in height_map.out_degree:
        if out >= 1:
            continue

        risk += height_map.nodes[u]["height"] + 1

    return risk


@tools.solution(part=2)
def find_largest_three_basins(height_map: nx.DiGraph) -> int:
    graph = nx.Graph(height_map.edges)
    basins = [len(basin) for basin in nx.connected_components(graph)]

    return prod(sorted(basins, reverse=True)[:3])


if __name__ == "__main__":
    solve()
