#!/usr/bin/env python3

import argparse
from collections import Counter
import logging
from logging import debug, info, warn
from pathlib import Path
import sys


def solve(datafile):
    pairs = [tuple(int(t) for t in line.strip().split()) for line in datafile]
    list1, list2 = zip(*pairs)
    counts = Counter(list2)
    
    tally = 0
    for val in list1:
        tally += val * counts[val]
    
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
    assert solve(datafile) == 31


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 18934359


if __name__ == "__main__":
    main()
