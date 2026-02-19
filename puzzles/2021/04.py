"""Advent of Code 2021 Day 4: Giant Squid"""

import itertools as it
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cached_property
from typing import Self

from advent_of_code import grid_utils as gru
from advent_of_code import reader, tools

YEAR, DAY, TEST = 2021, 4, False


@dataclass
class BingoBoard:
    board: list[list[str]]
    call_order: dict[str, int]

    @classmethod
    def parse_lines(cls, lines: Iterator[str], call_order: dict[str, int]) -> Self:
        return cls([line.split() for line in lines], call_order)

    @cached_property
    def digits(self) -> set[str]:
        return set(it.chain(*self.board))

    @cached_property
    def called_digits(self) -> set[str]:
        winning_turn = self.winning_turn

        return set(d for d in self.digits if self.call_order[d] <= winning_turn)

    @cached_property
    def uncalled_digits(self) -> set[str]:
        return self.digits.difference(self.called_digits)

    @cached_property
    def winning_digit(self) -> str:
        for d, turn in self.call_order.items():
            if turn == self.winning_turn:
                return d

        raise ValueError("Board is unwinnable")

    @cached_property
    def winning_turn(self) -> int:
        all_lines = it.chain(self.board, gru.transpose(self.board))

        return min(max(self.call_order[d] for d in line) for line in all_lines)

    def score(self) -> int:
        return sum(int(d) for d in self.uncalled_digits) * int(self.winning_digit)


def solve():
    input_data = reader.read_lines2(YEAR, DAY, test=TEST)
    ranked_bingo_boards = rank_bingo_boards(input_data)
    score_first_to_win(ranked_bingo_boards)
    score_last_to_win(ranked_bingo_boards)


@tools.solution(part=0)
def rank_bingo_boards(input_data: list[str]) -> list[BingoBoard]:
    call_order = parse_call_order(input_data[0])
    bingo_boards = parse_bingo_boards(input_data[2:], call_order)

    return sorted(bingo_boards, key=lambda bb: bb.winning_turn)


def parse_call_order(line: str) -> dict[str, int]:
    return {d: i for i, d in enumerate(line.split(","))}


def parse_bingo_boards(
    lines: list[str], call_order: dict[str, int]
) -> list[BingoBoard]:
    return [
        BingoBoard.parse_lines(g, call_order)
        for k, g in it.groupby(lines, lambda x: x != "")
        if k
    ]


@tools.solution(part=1)
def score_first_to_win(ranked_bingo_boards: list[BingoBoard]) -> int:
    return ranked_bingo_boards[0].score()


@tools.solution(part=2)
def score_last_to_win(ranked_bingo_boards: list[BingoBoard]) -> int:
    return ranked_bingo_boards[-1].score()


if __name__ == "__main__":
    solve()
