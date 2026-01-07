#!/usr/bin/env python3

import argparse
import logging
import sys
from itertools import islice
from pathlib import Path

from adventlib.grid import *

import pytest


def solve(datafile):
    grid = Grid([line.strip() for line in datafile.readlines()])

    tally = 0
    for cell, centre_val in grid.cells():
        if centre_val == '@' and sum(1 for _, value in grid.adjacent(cell) if value == '@') < 4:
            tally += 1

    return tally


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
    assert solve(datafile) == 13

def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 1551

if __name__ == "__main__":
    main()
