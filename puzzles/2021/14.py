"""Advent of Code 2021 Day 14: Extended Polymerization"""

from collections import Counter
from typing import TypeAlias

from advent_of_code import reader, tools

TemplateLike: TypeAlias = dict[str, tuple[str, ...]]


YEAR, DAY, TEST = 2021, 14, False
MIN_MAX = [min, max]


def solve():
    input_data = reader.read_lines2(YEAR, DAY, test=TEST)
    inital_polymer, polymer_templates = parse_input(input_data)
    ten_ticks(inital_polymer, polymer_templates)
    forty_ticks(inital_polymer, polymer_templates)


def parse_input(input_data: list[str]) -> tuple[str, list[str]]:
    return input_data[0], input_data[2:]


@tools.solution(part=1)
def ten_ticks(initial_polymer: str, polymer_templates: list[str]) -> int:
    initial_state = count_polymers(initial_polymer)
    template = create_polymer_template(polymer_templates)
    state = tick_many(initial_state, template, 10)
    elem_counter = count_elements(state, initial_polymer)
    min_val, max_val = [fn(elem_counter.values()) for fn in MIN_MAX]

    return max_val - min_val


@tools.solution(part=2)
def forty_ticks(initial_polymer: str, polymer_templates: list[str]) -> int:
    initial_state = count_polymers(initial_polymer)
    template = create_polymer_template(polymer_templates)
    state = tick_many(initial_state, template, 40)
    elem_counter = count_elements(state, initial_polymer)
    min_val, max_val = [fn(elem_counter.values()) for fn in MIN_MAX]

    return max_val - min_val


def count_polymers(text: str) -> Counter:
    counter = Counter()
    for left, right in zip(text[:-1], text[1:]):
        counter[left + right] += 1

    return counter


def create_polymer_template(lines: list[str]) -> TemplateLike:
    template = {}
    for line in lines:
        polymer, mid = line.split(" -> ")
        template[polymer] = tuple((polymer[0] + mid, mid + polymer[-1]))

    return template


def tick_many(initial_state: Counter, template: TemplateLike, ticks: int) -> Counter:
    state = initial_state
    for _ in range(ticks):
        state = tick(state, template)

    return state


def tick(state: Counter, template: TemplateLike) -> Counter:
    next_state = Counter()
    for polymer, val in state.items():
        next_state.update({np: val for np in template[polymer]})

    return next_state


def count_elements(state: Counter, initial_polymer: str) -> Counter:
    elements = Counter()
    for (char1, _), count in state.items():
        elements[char1] += count

    elements[initial_polymer[-1]] += 1

    return elements


if __name__ == "__main__":
    solve()
