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

    def create_blocking_location(corners, location, direction):
        print(f"Create blockage for {corners} in direction {direction}")
        match direction:
            case (0, -1):
                block = (corners[-1][0], min(corner[1] for corner in corners) - 1)
            case (0, 1):
                block = (corners[-1][0], max(corner[1] for corner in corners) + 1)
            case (-1, 0):
                block = (
                    min(corner[0] for corner in corners) - 1,
                    corners[-1][1],
                )
            case (1, 0):
                block = (
                    max(corner[0] for corner in corners) + 1,
                    corners[-1][1],
                )

        pl = location
        while pl != block:
            if blocked(*pl):
                return None
            pl = (pl[0] + direction[0], pl[1] + direction[1])
        return block

    turning_locations = []
    while inside_grid(*location):
        visited_locations.add(location)
        for _ in range(3):
            pending_location = (location[0] + direction[0], location[1] + direction[1])
            if not blocked(*pending_location):
                break
            direction = rotate(direction)
            turning_locations.append(location)
            if len(turning_locations) >= 3:
                print(
                    create_blocking_location(
                        turning_locations[-3:], location, direction
                    )
                )
        else:
            raise Exception("Spinning")
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
    assert solve(datafile) == 6


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == -1


if __name__ == "__main__":
    main()
