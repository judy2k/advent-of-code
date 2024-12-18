#!/usr/bin/env python3

import argparse
import logging
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
    return sum(
        solve_game(*(int(t) for t in match.groups()))
        for match in re.finditer(pat, datafile.read())  # type:ignore
    )


def score(a, b):
    return a * A_COST + b * B_COST


def solve_game(ax, ay, bx, by, target_x, target_y):
    max_a = min(target_x // ax, target_y // ay)

    return min(
        [
            score(a, remain_x // bx)
            for (a, remain_x, remain_y) in (
                (a, target_x - a * ax, target_y - a * ay)
                for a in range(0, max_a + 1)
            )
            if (
                remain_x % bx == 0
                and remain_y % by == 0
                and remain_x // bx == remain_y // by
            )
        ]
        or [0]
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
    assert solve(datafile) == 480


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 40069


def test_solve_game():
    assert solve_game(3, 5, 7, 11, 3 * 17, 5 * 17) == 17 * 3


if __name__ == "__main__":
    main()
