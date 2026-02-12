import itertools as it
from collections.abc import Generator, Sequence
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Self, TypeAlias

AnyGrid: TypeAlias = Sequence[Sequence[Any]]
AnyRaggedGrid: TypeAlias = Sequence[Sequence[Any]]

ORTHOGONAL_DELTAS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIAGONAL_DELTAS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]


@dataclass(frozen=True, order=True)
class Point:
    i: int
    j: int

    @property
    def norm_l1(self) -> int:
        return abs(self.i) + abs(self.j)

    def __add__(self, other: Self) -> Self:
        return type(self)(self.i + other.i, self.j + other.j)

    def __sub__(self, other: Self) -> Self:
        return type(self)(self.i - other.i, self.j - other.j)

    def __mul__(self, scalar: int) -> Self:
        return type(self)(self.i * scalar, self.j * scalar)

    def __contains__(self, val: int) -> bool:
        return self.i == val or self.j == val

    def __iter__(self) -> Generator[int, Any, None]:
        yield self.i
        yield self.j

    def as_tuple(self) -> tuple[int, ...]:
        return self.i, self.j

    def manhattan(self, other: Self) -> int:
        return abs(self.i - other.i) + abs(self.j - other.j)

    def get_neighbors(
        self, rows: int, cols: int, diagonals: bool = False
    ) -> Generator[Self, Any, None]:
        for delta in get_deltas() if diagonals else get_orthogonal_deltas():
            neighbor = self + delta
            if neighbor.is_within(rows, cols):
                yield neighbor

    def is_boundary(self, rows: int, cols: int) -> bool:
        return self.i in (0, rows - 1) or self.j in (0, cols - 1)

    def is_origin(self) -> bool:
        return self.i == 0 and self.j == 0

    def is_within(self, rows: int, cols: int) -> bool:
        return 0 <= self.i < rows and 0 <= self.j < cols


@dataclass(frozen=True, order=True)
class MovingPoint:
    pos: Point
    delta: Point = field(default_factory=lambda: Point(-1, 0))

    def is_within(self, rows: int, cols: int) -> bool:
        return self.pos.is_within(rows, cols)

    def next_pos(self) -> Point:
        return self.pos + self.delta

    def move(self) -> Self:
        return type(self)(self.next_pos(), self.delta)

    def rotate90(self, clockwise: bool = True) -> Self:
        i, j = self.delta
        new_delta = Point(j, -i) if clockwise else Point(-j, i)

        return type(self)(self.pos, new_delta)


@cache
def get_orthogonal_deltas() -> tuple[Point, ...]:
    return tuple(Point(i, j) for i, j in ORTHOGONAL_DELTAS)


@cache
def get_diagonal_deltas() -> tuple[Point, ...]:
    return tuple(Point(i, j) for i, j in DIAGONAL_DELTAS)


@cache
def get_deltas() -> tuple[Point, ...]:
    return tuple(Point(i, j) for i, j in ORTHOGONAL_DELTAS + DIAGONAL_DELTAS)


# --- Grid Utilities --- #


def find_one(grid: AnyGrid, target: Any) -> Point:
    return next(search(grid, target))


def is_square(grid: AnyGrid) -> bool:
    return len(grid) == len(grid[0])


def generate_edges(grid: AnyGrid, diagonals: bool = False):
    r, c = shape(grid)
    for u in generate_points(grid):
        for v in u.get_neighbors(r, c, diagonals):
            if v.is_within(r, c):
                yield u, v


def generate_points(grid: AnyGrid) -> Generator[Point, Any, None]:
    r, c = shape(grid)

    return (Point(i, j) for i, j in it.product(range(r), range(c)))


def generate_point_values(grid: AnyGrid) -> Generator[tuple[Point, Any], Any, None]:
    return ((p, value_at(grid, p)) for p in generate_points(grid))


def parse_grid(grid: AnyGrid, transform=lambda x: x) -> AnyGrid:
    return [[transform(char) for char in line] for line in grid]


def parse_to_dict(grid: AnyGrid, transform=lambda x: x) -> dict[Point, Any]:
    return {point: transform(val) for point, val in generate_point_values(grid)}


def search(grid: AnyGrid, target: Any) -> Generator[Point, None, None]:
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == target:
                yield Point(i, j)


def rotate(grid: AnyGrid) -> AnyGrid:
    return [[item for item in line] for line in zip(*grid[::-1])]


def rotate_diagonal(grid: AnyGrid) -> AnyRaggedGrid:
    k, n = 0, len(grid)
    rotated = []
    while k < 2 * n - 1:
        diag = [grid[i][k - i] for i in range(n) if 0 <= k - i < n]
        rotated.append(diag)
        k += 1

    return rotated


def shape(grid: AnyGrid) -> tuple[int, int]:
    return len(grid), len(grid[0])


def transpose(grid: AnyGrid) -> AnyGrid:
    return [[item for item in row] for row in it.zip_longest(*grid)]


def value_at(grid: AnyGrid, p: Point) -> Any:
    """Safe or direct access helper."""
    return grid[p.i][p.j]
