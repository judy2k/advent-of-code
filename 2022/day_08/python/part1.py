#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import sys

from itertools import chain, repeat
from functools import reduce
from operator import __or__


def solve_map(map):
    w = len(map[0])
    h = len(map)

    visibility = [[False] * w for _ in range(h)]
    lines = chain(
        [[(x, y) for x in reversed(range(w))] for y in range(h)],
        [[(x, y) for x in range(w)] for y in range(h)],
        [[(x, y) for y in reversed(range(h))] for x in range(w)],
        [[(x, y) for y in range(h)] for x in range(w)],
    )

    for line in lines:
        max_height = -1
        for x, y in line:
            if map[y][x] > max_height:
                max_height = map[y][x]
                visibility[y][x] = True

    return sum(cell for row in visibility for cell in row)


def solve(datafile):
    map = [[int(c) for c in line.strip()] for line in datafile]

    return solve_map(map)


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


def test_sample():
    sample_file = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(sample_file) == 21


def test_input():
    input_file = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(input_file) == 1805


if __name__ == "__main__":
    main()
