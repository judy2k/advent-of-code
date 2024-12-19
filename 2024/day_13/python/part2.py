#!/usr/bin/env python3

import argparse
import logging
import math
import re
import sys
from pathlib import Path
from typing import TextIO

A_COST = 3
B_COST = 1


def solve(datafile: TextIO):
    pat = r"""Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)"""
    games = list(re.finditer(pat, datafile.read()))

    return sum(
        solve_game(*(int(t) for t in match.groups()))
        for match in games  # type:ignore
    )


def score(a, b):
    return a * A_COST + b * B_COST


def solve_game(ax, ay, bx, by, target_x, target_y):
    target_x += 10_000_000_000_000
    target_y += 10_000_000_000_000

    if ax / ay == bx / by:
        raise Exception(
            "This algorithm doesn't work when A and B gradients are the same."
        )

    j = (target_x * ay - target_y * ax) / (bx * ay - by * ax)
    i = (target_x - j * bx) / ax

    if math.floor(i) == i and math.floor(j) == j:
        return score(int(i), int(j))
    return 0


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
    assert solve(datafile) == 875318608908


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 71493195288102


if __name__ == "__main__":
    main()
