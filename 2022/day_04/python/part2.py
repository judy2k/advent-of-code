#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

import re


def parse_ranges(line):
    return [int(s) for s in re.split(r"[-,]", line)]


def overlaps(a, b, c, d):
    return (a <= c and b >= c) or (c <= a and d >= a)


def solve(datafile):
    return sum(overlaps(*parse_ranges(line)) for line in datafile)


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("datafile", type=argparse.FileType(mode="r"))

    args = ap.parse_args(argv)

    logging.basicConfig(format="%(message)s", level=logging.DEBUG if args.verbose else logging.WARNING)
    print(solve(args.datafile))


def test_sample():
    assert parse_ranges("2-4,6-8\n") == [2, 4, 6, 8]
    assert overlaps(2, 8, 3, 7) == True
    assert overlaps(6, 6, 4, 6) == True
    assert overlaps(2, 6, 4, 8) == True
    assert list(overlaps(*parse_ranges(line)) for line in open("../sample.txt")) == [
        False,
        False,
        True,
        True,
        True,
        True,
    ]
    assert solve(open("../sample.txt")) == 4


if __name__ == "__main__":
    main()
