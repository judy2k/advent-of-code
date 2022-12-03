#!/usr/bin/env python3

import argparse
from functools import lru_cache
import logging
from logging import debug, info, warn
import sys

from enum import Enum


class Shape(Enum):
    ROCK = ("AX", 1)
    SCISSORS = ("CZ", 3)
    PAPER = ("BY", 2)

    def __init__(self, letters, score):
        self.score = score
        self.letters = letters

    @property
    @lru_cache
    def beats(self):
        shapes = list(self.__class__)
        return shapes[(shapes.index(self) + 1) % len(shapes)]

    @classmethod
    def lookup(cls, letter):
        if getattr(cls, "__lookup", None) is None:
            cls.__lookup = {l: s for s in cls for l in s.letters}
        return cls.__lookup[letter]


def score(theirs: Shape, mine: Shape) -> int:
    s = mine.score + (6 if mine.beats is theirs else 3 if mine is theirs else 0)
    info(f"{mine}, {theirs}: {s}")
    return s


def solve(datafile) -> int:
    return sum(score(*[Shape.lookup(l) for l in line.split()]) for line in datafile)


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("datafile", type=argparse.FileType(mode="r"))

    args = ap.parse_args(argv)

    logging.basicConfig(format="%(message)s", level=logging.DEBUG if args.verbose else logging.WARNING)
    print(solve(args.datafile))


def test_sample():
    assert solve(open("../sample.txt")) == 15


# def test_draws():
#     assert score(Shape.ROCK, Shape.ROCK) == 2
#     assert score(Shape.PAPER, Shape.PAPER) == 4
#     assert score(Shape.SCISSORS, Shape.SCISSORS) == 6


# def test_wins():
#     assert score(Shape.ROCK, Shape.PAPER) == 2
#     assert score(Shape.PAPER, Shape.SCISSORS) == 4
#     assert score(Shape.SCISSORS, Shape.ROCK) == 6


if __name__ == "__main__":
    main()
