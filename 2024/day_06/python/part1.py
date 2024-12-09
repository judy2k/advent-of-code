#!/usr/bin/env python3

import argparse
import logging
import sys
from pathlib import Path

DIRECTIONS = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]


def solve(datafile):
    direction = (-1, 0)
    visited_locations = set()
    grid = [line.strip() for line in datafile]
    grid_height = len(grid)
    grid_width = len(grid[0])

    for i, row in enumerate(grid):
        if "^" in row:
            location = (i, row.index("^"))
            break
    grid[location[0]] = grid[location[0]].replace("^", ".")

    def inside_grid(row, col):
        return 0 <= row < grid_height and 0 <= col < grid_width

    def blocked(row, col):
        return inside_grid(row, col) and grid[row][col] == "#"

    def rotate(direction):
        return DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 4]

    while inside_grid(*location):
        visited_locations.add(location)
        pending_location = (location[0] + direction[0], location[1] + direction[1])
        if blocked(*pending_location):
            direction = rotate(direction)
        else:
            location = pending_location

    return len(visited_locations)


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
    assert solve(datafile) == 41


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 4973


if __name__ == "__main__":
    main()
