#!/usr/bin/env python3

import argparse
from functools import lru_cache
import logging
from logging import debug, info, warn
import sys


class Shape:
    lookup = {}
    shapes = []

    def __init__(self, name, letters, score):
        self.name = name
        self.score = score
        for l in letters:
            self.lookup[l] = self
        self.shapes.append(self)
        self.beats_index = len(self.shapes)

    @property
    @lru_cache
    def beats(self):
        return self.shapes[self.beats_index % len(self.shapes)]

    def __repr__(self):
        return f"Shape({self.name})"


ROCK = Shape("rock", "AX", 1)
SCISSORS = Shape("scissors", "CZ", 3)
PAPER = Shape("paper", "BY", 2)


def score(theirs, mine):
    return mine.score + (6 if mine.beats is theirs else mine.score if mine is theirs else 0)


def solve(datafile):
    return sum(score(*[Shape.lookup[l] for l in line.split()]) for line in datafile)


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("datafile", type=argparse.FileType(mode="r"))

    args = ap.parse_args(argv)

    logging.basicConfig(format="%(message)s", level=logging.DEBUG if args.verbose else logging.WARNING)
    print(solve(args.datafile))


def test_sample():
    assert solve(open("../sample.txt")) == 15


if __name__ == "__main__":
    main()
