#!/usr/bin/env python3

import argparse
import logging
import sys
from pathlib import Path

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def solve(datafile):
    grid = [[int(c) for c in line.strip()] for line in datafile]

    trailheads = []
    for row_n, row in enumerate(grid):
        for col_n, val in enumerate(row):
            if val == 0:
                trailheads.append((row_n, col_n))

    return sum(count_peaks(start, grid) for start in trailheads)


def count_peaks(pos, grid):
    val = grid[pos[0]][pos[1]]
    if val == 9:
        return 1
    return sum(
        count_peaks(candidate, grid)
        for candidate in [
            (pos[0] + option[0], pos[1] + option[1]) for option in DIRECTIONS
        ]
        if 0 <= candidate[0] < len(grid)
        and 0 <= candidate[1] < len(grid[0])
        and grid[candidate[0]][candidate[1]] == val + 1
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


def test_sample2():
    datafile = Path(__file__).parent.parent.joinpath("sample2.txt").open()
    assert solve(datafile) == 81


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 1497


if __name__ == "__main__":
    main()
