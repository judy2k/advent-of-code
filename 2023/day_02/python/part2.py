#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

from functools import reduce
from operator import mul
import re


def parse_line(line):
    match = re.match(r"Game (?P<id>\d+): (?P<groupstr>.*)", line)
    return reduce(
        mul,
        combine_subsets(parse_subset(gs) for gs in match.group("groupstr").split("; ")),
    )


def parse_subset(subset):
    return (
        int((m := re.search(r"(\d+) red", subset)) and m.group(1) or 0),
        int((m := re.search(r"(\d+) green", subset)) and m.group(1) or 0),
        int((m := re.search(r"(\d+) blue", subset)) and m.group(1) or 0),
    )


def combine_subsets(subsets):
    return tuple(max(vs) for vs in zip(*subsets))


def solve(datafile):
    return sum(parse_line(line) for line in datafile)


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


from pathlib import Path


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 2286


def test_parse_subset():
    assert parse_subset("3 blue, 4 red") == (4, 0, 3)
    assert parse_subset("1 red, 2 green, 6 blue") == (1, 2, 6)


def test_combine_subsets():
    assert combine_subsets([(4, 0, 3), (1, 2, 6)]) == (4, 2, 6)


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 63542


def test_power():
    assert parse_line("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green") == 48


if __name__ == "__main__":
    main()
