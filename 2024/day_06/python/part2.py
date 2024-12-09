#!/usr/bin/env python3

import argparse
import logging
import sys
from itertools import product
from pathlib import Path

DIRECTIONS = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]


def solve_grid(grid, location, blocked_location):
    if grid[blocked_location[0]][blocked_location[1]] == "#":
        return False

    grid_height = len(grid)
    grid_width = len(grid[0])

    direction = (-1, 0)
    visited_locations = set()

    def inside_grid(row, col):
        return 0 <= row < grid_height and 0 <= col < grid_width

    def blocked(row, col):
        return inside_grid(row, col) and (
            grid[row][col] == "#" or blocked_location == (row, col)
        )

    def rotate(direction):
        return DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 4]

    while inside_grid(*location):
        visited_locations.add((location, direction))
        pending_location = (location[0] + direction[0], location[1] + direction[1])
        if blocked(*pending_location):
            direction = rotate(direction)
        else:
            if (pending_location, direction) in visited_locations:
                return True
            location = pending_location

    return False


def solve(datafile):
    grid = [list(line.strip()) for line in datafile]
    grid_height = len(grid)
    grid_width = len(grid[0])

    for i, row in enumerate(grid):
        if "^" in row:
            location = (i, row.index("^"))
            grid[location[0]][location[1]] = "."
            break

    tally = 0
    for row, col in product(range(grid_height), range(grid_width)):
        if solve_grid(grid, location, (row, col)):
            tally += 1

    return tally


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
