"""Advent of Code 2021 Day 13: Transparent Origami"""

import itertools as it
import re
from dataclasses import dataclass
from typing import Self, TypeAlias

from advent_of_code import reader, tools

CoordLike: TypeAlias = tuple[int, ...]


YEAR, DAY, TEST = 2021, 13, False


@dataclass
class Fold:
    is_x: bool
    scale: int

    @classmethod
    def parse_text(cls, txt) -> Self:
        m = re.search(r"\w=\d+", txt)
        if m is None:
            raise ValueError("No match found!")

        axis, digit = m.group().split("=")

        return cls(axis == "x", int(digit))

    def do_fold(self, point: CoordLike) -> CoordLike:
        x, y = point
        if self.is_x and self.scale <= x:
            return 2 * self.scale - x, y

        if not self.is_x and self.scale <= y:
            return x, 2 * self.scale - y

        return x, y


def solve():
    input_data = reader.read_lines2(YEAR, DAY, test=TEST)
    paper, folds = parse_input(input_data)
    one_fold(paper, folds[0])
    view_result(paper, folds)


@tools.solution(part=0)
def parse_input(input_data: list[str]) -> tuple[set[CoordLike], list[Fold]]:
    points, folds = [list(g) for k, g in it.groupby(input_data, lambda x: x != "") if k]

    return collect_points(points), collect_folds(folds)


def collect_points(lines: list[str]) -> set[CoordLike]:
    paper = set()
    for line in lines:
        i, j = re.findall(r"\d+", line)
        paper.add((int(i), int(j)))

    return paper


def collect_folds(lines: list[str]) -> list[Fold]:
    return [Fold.parse_text(line) for line in lines]


@tools.solution(part=1)
def one_fold(paper: set[CoordLike], fold: Fold) -> int:
    return len(set(fold.do_fold(point) for point in paper))


@tools.solution(part=2)
def view_result(paper: set[CoordLike], folds: list[Fold]) -> str:
    final_paper = many_folds(paper, folds)

    return display(final_paper)


def many_folds(paper: set[CoordLike], folds: list[Fold]) -> set[CoordLike]:
    current = paper
    for fold in folds:
        current = set(fold.do_fold(point) for point in current)

    return current


def display(paper: set[CoordLike]) -> str:
    grid = make_grid(paper)
    for x, y in paper:
        grid[y][x] = "■"

    text = ""
    for line in grid:
        text += "\n" + "".join(line)

    return text


def make_grid(paper: set[CoordLike], fillval: str = " ") -> list[list[str]]:
    x_max = max(p[0] for p in paper) + 1
    y_max = max(p[1] for p in paper) + 1

    return [[fillval for _ in range(x_max)] for __ in range(y_max)]


if __name__ == "__main__":
    solve()
