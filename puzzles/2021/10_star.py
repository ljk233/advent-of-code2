"""Advent of Code 2021 Day 10: Syntax Scoring"""

import functools
from statistics import median

from advent_of_code import reader, tools

YEAR, DAY, TEST = 2021, 10, False

CLOSES = {")": "(", "]": "[", "}": "{", ">": "<"}
CORRUPT = {")": 3, "]": 57, "}": 1197, ">": 25137}
OPENS = {"(": ")", "[": "]", "{": "}", "<": ">"}
AUTOCOMPLETE = {b: i for i, b in enumerate("([{<", start=1)}


def solve():
    input_data = reader.read_lines2(YEAR, DAY, test=TEST)
    calculate_corruption_score(input_data)
    calculate_autocompletion_score(input_data)


@tools.solution(part=1)
def calculate_corruption_score(input_data: list[str]) -> int:
    return sum(corruption_score(line)[0] for line in input_data)


@tools.solution(part=2)
def calculate_autocompletion_score(input_data: list[str]) -> int:
    auto_scores = [autocompletion_score(line) for line in input_data]

    return int(median(score for score in auto_scores if score != 0))


@functools.cache
def corruption_score(line: str) -> tuple[int, tuple[str, ...]]:
    open_brackets = []
    for candidate in line:
        if not is_closing(candidate):
            open_brackets.append(candidate)
            continue

        if not open_brackets or not closes(open_brackets[-1], candidate):
            return CORRUPT[candidate], tuple(open_brackets)

        open_brackets.pop()

    return 0, tuple(open_brackets)


@functools.cache
def autocompletion_score(line: str) -> int:
    corruption, open_brackets = corruption_score(line)
    if corruption >= 1:
        return 0

    total = 0
    for bracket in reversed(open_brackets):
        total = (total * 5) + AUTOCOMPLETE[bracket]

    return total


def is_closing(bracket: str) -> bool:
    return bracket in CLOSES


def closes(opened: str, candidate: str) -> bool:
    return opened == CLOSES[candidate]


if __name__ == "__main__":
    solve()
