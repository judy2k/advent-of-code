#!/usr/bin/env python3

import argparse
import logging
import sys
from pathlib import Path


def pointings(instructions):
    points_at = 50
    for instruction in instructions:
        points_at = (points_at + (int(instruction[1:]) if instruction[0] == 'R' else -int(instruction[1:]))) % 100
        yield points_at


def solve(datafile):
    return len(list(filter(lambda p: p == 0, pointings(line.strip() for line in datafile))))


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
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
    assert solve(datafile) == 3

def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 1066


if __name__ == "__main__":
    main()
