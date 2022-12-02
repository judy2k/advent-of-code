#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys


class Shape:
    shapes = None

    def __init__(self, name, letters, score):
        self.name = name
        self.letters = set(list(letters))
        self.beats = None
        self.score = score

    @classmethod
    def from_letter(cls, letter):
        for shape in cls.shapes:
            if letter in shape.letters:
                return shape

    def __repr__(self):
        return f"Shape({self.name})"


ROCK = Shape("rock", "AX", 1)
PAPER = Shape("paper", "BY", 2)
SCISSORS = Shape("scissors", "CZ", 3)

ROCK.beats = SCISSORS
SCISSORS.beats = PAPER
PAPER.beats = ROCK

Shape.shapes = [ROCK, PAPER, SCISSORS]


def score(theirs, mine):
    if mine.beats is theirs:
        return mine.score + 6
    elif mine is theirs:
        return mine.score * 2
    else:
        return mine.score


def solve(datafile):
    return sum(score(*[Shape.from_letter(l) for l in line.split()]) for line in datafile)


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
