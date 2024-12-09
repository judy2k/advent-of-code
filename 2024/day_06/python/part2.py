#!/usr/bin/env python3

import argparse
import logging
import sys
from itertools import product
from pathlib import Path

from tqdm import tqdm


class Grid:
    def __init__(self, rows: list[list[str]]):
        self.location = (-1, -1)
        self.height = len(rows)
        self.width = len(rows[0])
        self.blocks = set()
        for row, col in product(range(self.height), range(self.width)):
            if rows[row][col] == "#":
                self.blocks.add((row, col))
            elif rows[row][col] == "^":
                self.location = (row, col)

    def inside(self, location):
        row, col = location
        return 0 <= row < self.height and 0 <= col < self.width

    def blocked(self, location):
        return self.inside(location) and location in self.blocks


DIRECTIONS = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]


def solve_grid(grid: Grid, blocked_location):
    if grid.blocked(blocked_location):
        return False

    location = grid.location
    direction = (-1, 0)
    visited_locations = set()

    def rotate(direction):
        return DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 4]

    while grid.inside(location):
        if (location, direction) in visited_locations:
            return True
        visited_locations.add((location, direction))
        pending_location = (location[0] + direction[0], location[1] + direction[1])
        if (
            grid.blocked(pending_location)
            or pending_location == blocked_location
        ):
            direction = rotate(direction)
        else:
            location = pending_location

    return {visited_location[0] for visited_location in visited_locations}


def solve(datafile):
    grid = Grid([list(line.strip()) for line in datafile])

    return sum(
        1
        for r in (
            solve_grid(grid, block)
            for block in tqdm(solve_grid(grid, (-1, -1)))
        )
        if r is True
    )


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("datafile", type=argparse.FileType(mode="r"))

    args = ap.parse_args(argv)

    logging.basicConfig(
        format="%(message)s",
        level=logging.DEBUG if args.verbose else logging.WARNING,
    )
    print(solve(args.datafile))


# Tests ------------------------------------------------------------------------


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 6


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 1482


if __name__ == "__main__":
    main()
#
