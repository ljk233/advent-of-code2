"""Advent of Code 2021 Day 2: Dive!"""

from collections.abc import Callable
from dataclasses import dataclass, field, replace
from enum import Enum, auto
from functools import reduce
from math import prod
from typing import Self

from advent_of_code import grid_utils as gru
from advent_of_code import reader, tools

YEAR, DAY, TEST = 2021, 2, False


class Command(Enum):
    FORWARD = auto()
    DOWN = auto()
    UP = auto()


@dataclass(frozen=True)
class Instruction:
    cmd: Command
    value: int

    @classmethod
    def parse_text(cls, text: str) -> Self:
        cmd, val = text.split()

        return cls(get_command(cmd), int(val))

    def delta(self) -> gru.Point:
        return unit_delta(self.cmd) * self.value


@dataclass(frozen=True)
class AimingMovingPoint:
    point: gru.Point = field(default_factory=gru.origin_point)
    aim: int = field(default=0)

    def execute(self, instructuction: Instruction) -> Self:
        if instructuction.cmd == Command.FORWARD:
            new_point = replace(
                self.point,
                i=self.point.i + (self.aim * instructuction.value),
                j=self.point.j + instructuction.value,
            )

            return replace(self, point=new_point)

        return replace(self, aim=self.aim + instructuction.value)

    def as_tuple(self) -> tuple[int, ...]:
        return self.point.as_tuple()


def solve():
    input_data = reader.read_lines2(YEAR, DAY, test=TEST)
    instructions = parse_input_data(input_data)
    calculate_displacement(instructions)
    calculate_aimed_displacement(instructions)


@tools.solution(part=0)
def parse_input_data(input_data: list[str]) -> list[Instruction]:
    return [Instruction.parse_text(line) for line in input_data]


@tools.solution(part=1)
def calculate_displacement(instructions: list[Instruction]) -> int:
    def follow(submarine, instruction):
        return submarine + instruction.delta()

    final_submarine = follow_instuctions(instructions, gru.origin_point, follow)

    return prod(final_submarine.as_tuple())


@tools.solution(part=2)
def calculate_aimed_displacement(instructions: list[Instruction]) -> int:
    def follow(submarine, instruction):
        return submarine.execute(instruction)

    final_submarine = follow_instuctions(instructions, AimingMovingPoint, follow)

    return prod(final_submarine.point.as_tuple())


def follow_instuctions[T](
    instructions: list[Instruction],
    initial_submarine: Callable[[], T],
    follow_fn: Callable[[T, Instruction], T],
) -> T:
    return reduce(follow_fn, instructions, initial_submarine())


def get_command(cmd: str) -> Command:
    command_map = {
        "forward": Command.FORWARD,
        "down": Command.DOWN,
        "up": Command.UP,
    }

    command = command_map.get(cmd)
    if command is None:
        raise ValueError(f"Unable to parse cmd argument: {cmd=}")

    return command


def unit_delta(cmd: Command) -> gru.Point:
    unit_deltas = {
        Command.FORWARD: gru.Point(0, 1),
        Command.UP: gru.Point(-1, 0),
        Command.DOWN: gru.Point(1, 0),
    }
    return unit_deltas[cmd]


if __name__ == "__main__":
    solve()
