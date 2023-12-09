#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import re
import sys

from functools import reduce
from operator import mul


def ints(s):
    return [int(i) for i in re.findall(r"-?\d+", s)]


def count_winners(time, distance):
    return sum(1 for t in range(0, time + 1) if (time - t) * t > distance)


def parse(datafile):
    times = ints(datafile.readline())
    distances = ints(datafile.readline())
    return times, distances


def solve(datafile):
    times, distances = parse(datafile)

    return reduce(mul, (count_winners(t, d) for t, d in zip(times, distances)))


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


def test_parse():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    ts, ds = parse(datafile)
    assert ts == [7, 15, 30]
    assert ds == [9, 40, 200]


def test_ints():
    assert ints("12 -465 7 -3 422") == [12, -465, 7, -3, 422]


def test_count_winners():
    assert count_winners(7, 9) == 4


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 288


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 316800


if __name__ == "__main__":
    main()
