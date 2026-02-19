"""Advent of Code 2021 Day 8: Seven Segment Search"""

from collections.abc import Iterable

from advent_of_code import reader, tools

YEAR, DAY, TEST = 2021, 8, False


def solve():
    input_data = reader.read_lines2(YEAR, DAY, test=TEST)
    patterns, display_digits = parse_input_data(input_data)
    part1(display_digits)
    part2(display_digits, patterns)


@tools.solution(part=0)
def parse_input_data(
    input_data: list[str],
) -> tuple[list[list[set[str]]], list[list[str]]]:
    seven_digit_displays = [line.split(" | ") for line in input_data]
    patterns_str, display_patterns_str = zip(*seven_digit_displays)
    patterns = [parse_pattern(pattern_str) for pattern_str in patterns_str]
    display_digits = [parse_display(pattern) for pattern in display_patterns_str]

    return patterns, display_digits


@tools.solution(part=1)
def part1(display_digits: list[list[str]]) -> int:
    return sum(count_appearances(digits, 2, 3, 4, 7) for digits in display_digits)


@tools.solution(part=2)
def part2(display_digits: list[list[str]], patterns: list[list[set[str]]]) -> int:
    return sum(
        decode_display_digits(dd, patt) for dd, patt in zip(display_digits, patterns)
    )


def count_appearances(display: list[str], *lengths) -> int:
    return sum(1 for signature in display if len(signature) in lengths)


def parse_pattern(pattern: str) -> list[set[str]]:
    return [set(pattern) for pattern in pattern.split()]


def parse_display(display: str) -> list[str]:
    return [signature(pattern) for pattern in display.split()]


def decode_display_digits(display_digits: list[str], patterns: list[set[str]]) -> int:
    digit_pattern_map = map_digit_patterns(patterns)
    signature_digit_map = reverse_digit_pattern_map(digit_pattern_map)
    digits_str = "".join(signature_digit_map[sig] for sig in display_digits)
    return int(digits_str)


def map_digit_patterns(patterns: list[set[str]]) -> dict[str, set[str]]:
    digit_pattern = {}
    unique_counts = {2: "1", 3: "7", 4: "4", 7: "8"}
    for pattern in patterns:
        if len(pattern) in unique_counts:
            digit_pattern[unique_counts[len(pattern)]] = pattern

    for pattern in [p for p in patterns if len(p) == 6]:
        if not digit_pattern["1"].issubset(pattern):
            digit_pattern["6"] = pattern
        elif digit_pattern["4"].issubset(pattern):
            digit_pattern["9"] = pattern
        else:
            digit_pattern["0"] = pattern

    for pattern in [p for p in patterns if len(p) == 5]:
        if digit_pattern["1"].issubset(pattern):
            digit_pattern["3"] = pattern
        elif digit_pattern["6"].issuperset(pattern):
            digit_pattern["5"] = pattern
        else:
            digit_pattern["2"] = pattern

    return digit_pattern


def reverse_digit_pattern_map(digit_pattern_map: dict[str, set[str]]) -> dict[str, str]:
    return {signature(pattern): digit for digit, pattern in digit_pattern_map.items()}


def signature(pattern: Iterable[str]) -> str:
    return "".join(sorted(pattern))


if __name__ == "__main__":
    solve()
