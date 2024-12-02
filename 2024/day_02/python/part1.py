#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import sys


def solve(datafile):
    safe = 0

    for line in datafile:
        if is_safe([int(t) for t in line.strip().split()]):
            safe += 1

    return safe


def cmp(a, b):
    return (a > b) - (a < b)


def is_safe(ns: list[int]) -> bool:
    ts = list(zip(ns, ns[1:]))
    a, b = ts[0]
    direction = cmp(a, b)
    if direction == 0:
        return False

    for a, b in ts:
        if cmp(a, b) != direction:
            return False
        d = abs(a - b)
        if d < 1 or d > 3:
            return False

    return True


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
    assert solve(datafile) == 2


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 257


if __name__ == "__main__":
    main()
