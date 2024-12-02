#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import sys


def solve(datafile):
    pairs = [tuple(int(t) for t in line.strip().split()) for line in datafile]
    list1, list2 = zip(*pairs)
    sorted_pairs = zip(sorted(list1), sorted(list2))
    return sum(
        abs(a - b) for a, b in sorted_pairs
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
    assert solve(datafile) == 11


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 2378066


if __name__ == "__main__":
    main()
