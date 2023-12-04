#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

import re


def parse_subset(subset):
    return tuple(
        int((m := re.search(fr"(\d+) {color}", subset)) and m.group(1) or 0)
        for color in ("red", "green", "blue")
    )


def combine_subsets(subsets):
    return tuple(max(vs) for vs in zip(*subsets))

def parse_line(line):
     match = re.match(r"Game (?P<id>\d+): (?P<groupstr>.*)", line)
     return int(match.group("id")), match.group("groupstr").split("; ")

def solve(datafile):
    bag = (12, 13, 14)
    tally = 0
    
    for line in datafile:
        id, groupstrs = parse_line(line)
        totals = combine_subsets([parse_subset(gs) for gs in groupstrs])
        if all(a >= b for a, b in zip(bag, totals)):
            debug("Adding %d", id)
            tally += id

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


from pathlib import Path


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 8


def test_parse_subset():
    assert parse_subset("3 blue, 4 red") == (4, 0, 3)
    assert parse_subset("1 red, 2 green, 6 blue") == (1, 2, 6)


def test_combine_subsets():
    assert combine_subsets([(4, 0, 3), (1, 2, 6)]) == (4, 2, 6)


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 2268


if __name__ == "__main__":
    main()
