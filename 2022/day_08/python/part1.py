#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import sys

from functools import reduce
from operator import __or__


def solve_map(map):
    w = len(map[0])
    h = len(map)

    visibility = [[False] * w for _ in range(h)]

    max_height = -1

    def update_visibility(r, c):
        nonlocal max_height
        height = map[r][c]
        if height > max_height:
            max_height = height
            visibility[r][c] = True

    def vs(heights):
        mh = -1
        for height in heights:
            if height > mh:
                mh = height
                yield True
            else:
                yield False

    # left to right
    for r in range(h):
        for c, v in zip(
            range(w),
            vs([map[r][c] for c in range(w)]),
        ):
            visibility[r][c] |= v

    # top to bottom
    for c in range(w):
        for r, v in zip(
            range(h),
            vs([map[r][c] for r in range(h)]),
        ):
            visibility[r][c] |= v

    # right to left
    for r in range(h):
        for c, v in zip(
            reversed(range(w)),
            vs([map[r][c] for c in reversed(range(w))]),
        ):
            visibility[r][c] |= v

    # bottom to top
    for c in range(w):
        for r, v in zip(
            reversed(range(h)),
            vs([map[r][c] for r in reversed(range(h))]),
        ):
            visibility[r][c] |= v

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
