"""Provides classes for working with two-dimensional grids of data."""

from collections.abc import Callable, Generator, Iterable
from dataclasses import dataclass
from functools import total_ordering
from itertools import product
from typing import NamedTuple, TextIO, TypeVar

__all__ = ["Grid", "Location", "Direction", "UP", "DOWN", "LEFT", "RIGHT"]

T = TypeVar("T", default=str)


class OutOfBoundsError(Exception):
    def __init__(self, row, col, grid):
        super().__init__(
            f"({row}, {col}) is outside the Grid bounds of ({grid.height}, {grid.width})"
        )
        self.row = row
        self.col = col
        self.grid = grid


def _identity(val: T) -> T:
    """Identity function - returns the argument that was passed in, unchanged."""
    return val


@dataclass
@total_ordering
class Location(Iterable):
    """The location of a cell in a grid."""

    row: int
    col: int

    def move(self, direction: "Direction") -> "Location":
        """Return a Location representing the cell in the direction passed in."""
        return Location(self.row + direction.row, self.col + direction.col)

    def adjacent(
        self, include_diagonals: bool = True, include_centre: bool = True
    ) -> Generator["Location"]:
        """Iterate over all the adjacent locations.

        Locations with a negative row or column will not be generated.

        include_diagonals: bool -- Include diagonally adjacent locations.
        include_centre: bool -- Include the current location as well as adjacent locations.
        """

        if include_diagonals:
            for row, col in product(
                range(max(0, self.row - 1), self.row + 2),
                range(max(0, self.col - 1), self.col + 2),
            ):
                if Location(row, col) != self or include_centre:
                    yield Location(row, col)
        else:
            for direction in Direction.all():
                loc = self + direction
                if loc.row >= 0 and loc.col >= 0:
                    yield loc
            if include_centre:
                yield self

    def __add__(self, direction: "Direction") -> "Location":
        """Locations can be added to a provided Direction to obtain a new Location."""
        return Location(self.row + direction.row, self.col + direction.col)

    def __iter__(self):
        """This allows unpacking the values in a Location."""
        return iter([self.row, self.col])

    def __eq__(self, other):
        """Test for equality with another Location."""
        return self.row == other.row and self.col == other.col

    def __lt__(self, other):
        """Allow locations to be sorted by row, then column."""
        if self.row < other.row:
            return True
        elif self.row == other.row:
            return self.col < other.col


class Direction(NamedTuple):
    """A direction to look or move in."""

    row: int
    col: int

    @staticmethod
    def all() -> list["Direction"]:
        """Return a list of all Direction instances, starting with UP, and rotating clockwise."""
        return [UP, RIGHT, DOWN, LEFT]

    def clockwise(self) -> "Direction":
        """Return the Direction 90° clockwise to this one."""
        return Direction(self.col, -1 * self.row)

    def anticlockwise(self) -> "Direction":
        """Return the Direction 90° anticlockwise to this one."""
        return Direction(-1 * self.col, self.row)

    def __eq__(self, other):
        """Allow two Directions to be tested for equality."""
        return self.row == other.row and self.col == other.col


UP = Direction(-1, 0)
RIGHT = Direction(0, 1)
DOWN = Direction(1, 0)
LEFT = Direction(0, -1)


class Grid[T]:
    """A two-dimensional grid of cells.

    Keyword arguments:
    rows -- A list of rows. Each row should also be a list of cells in that row.
    """

    rows: list[list[T]]

    def __init__(self, rows: list[list[T]]):
        """Initialize a Grid from the provided row data."""
        self.rows = rows

    @classmethod
    def read(
        cls, input_file: TextIO, converter: None | Callable[[str], T] = None
    ) -> "Grid[T]":
        """Read in a space-separated grid from a file-type object."""
        transform = _identity if converter is None else converter

        rows = [
            [transform(t) for t in line.strip().split()] for line in input_file
        ]
        return cls(rows)

    def cells(self) -> Generator[tuple[Location, T]]:
        """Returns an iterator over all the cells in the grid."""
        for row, col in product(range(self.height), range(self.width)):
            yield Location(row, col), self[row, col]  # type: ignore

    def adjacent(
        self,
        centre: Location,
        include_diagonals: bool = True,
        include_centre: bool = False,
    ) -> Generator[tuple[Location, T]]:
        """Iterate over all the adjacent locations and their values in the grid.

        include_diagonals: bool -- Include diagonally adjacent locations.
        include_centre: bool -- Include the current location as well as adjacent locations.
        """
        for location in centre.adjacent(
            include_centre=include_centre, include_diagonals=include_diagonals
        ):
            if self.in_bounds(location):
                yield location, self[location]  # type: ignore

    def in_bounds(
        self, row_or_location: int | Location, col: int | None = None
    ) -> bool:
        """
        Determine if a location is valid within the grid.

        Usage:
            in_bounds(loc: Location) -> bool
            in_bounds(row: int, col: int) -> bool
        """

        if isinstance(row_or_location, Location) and col is None:
            row, col = row_or_location
        else:
            row = row_or_location  # type: ignore
        return 0 <= row < self.height and 0 <= col < self.width  # type: ignore

    @property
    def height(self) -> int:
        """The number of rows in the grid."""
        return len(self.rows)

    @property
    def width(self) -> int:
        """The number of cols in the grid."""

        return len(self.rows[0]) if self.rows else 0

    def __getitem__(self, loc: Location | tuple[int, int]) -> T | None:
        """Obtain a cell's contents at a specified location."""

        row, col = loc
        if self.in_bounds(row, col):
            return self.rows[row][col]
        return None

    def __setitem__(
        self, loc: Location | tuple[int, int], value: T
    ) -> T | None:
        """Set a cell's contents at a specified location.

        If the loc is outside of the Grid's width and height, an OutOfBoundsError will be raised."""

        row, col = loc
        if self.in_bounds(row, col):
            self.rows[row][col] = value
        else:
            raise OutOfBoundsError(row, col, self)
