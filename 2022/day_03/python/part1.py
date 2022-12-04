#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

from string import ascii_letters

scores = {l: i for i, l in enumerate(ascii_letters, start=1)}


def score_line(rucksack):
    pivot = len(rucksack) // 2
    return scores[(set(rucksack[:pivot]).intersection(rucksack[pivot:])).pop()]


def solve(datafile):
    return sum(score_line(line.strip()) for line in datafile)


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("datafile", type=argparse.FileType(mode="r"))

    args = ap.parse_args(argv)

    logging.basicConfig(format="%(message)s", level=logging.DEBUG if args.verbose else logging.WARNING)
    print(solve(args.datafile))


def test_sample():
    assert solve(open("../sample.txt")) == 157
    assert solve(open("../input.txt")) == 7875


if __name__ == "__main__":
    main()
