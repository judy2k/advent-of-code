#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import re
import sys

from bisect import bisect_left


class Calc:
    def __init__(self, time):
        self._time = time

    def __len__(self):
        return self._time + 1

    def __getitem__(self, i):
        return (self._time - i) * i


def joined_int(s):
    return int("".join(re.findall(r"-?\d+", s)))


def count_winners(time, distance):
    return time + 1 - bisect_left(Calc(time), distance) * 2


def parse(datafile):
    time = joined_int(datafile.readline())
    distance = joined_int(datafile.readline())
    return time, distance


def solve(datafile):
    time, distance = parse(datafile)

    return count_winners(time, distance)


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
    assert ts == 71530
    assert ds == 940200


def test_count_winners():
    assert count_winners(7, 9) == 4


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 71503


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 45647654


if __name__ == "__main__":
    main()
