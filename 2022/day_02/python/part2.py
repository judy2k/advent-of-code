#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys


SCORES = {
    "A X": 0 + 3,  # ROCK + LOSE = SCISSORS (3)
    "A Y": 3 + 1,  # ROCK + DRAW = ROCK (1)
    "A Z": 6 + 2,  # ROCK + WIN = PAPER (2)
    "B X": 0 + 1,  # PAPER + LOSE = ROCK (1)
    "B Y": 3 + 2,  # PAPER + DRAW = PAPER (2)
    "B Z": 6 + 3,  # PAPER + WIN = SCISSORS (3)
    "C X": 0 + 2,  # SCISSORS + LOSE = PAPER (2)
    "C Y": 3 + 3,  # SCISSORS + DRAW = SCISSORS (3)
    "C Z": 6 + 1,  # SCISSORS + WIN = ROCK (1)
}


def solve(datafile) -> int:
    return sum(SCORES[line.strip()] for line in datafile)


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("datafile", type=argparse.FileType(mode="r"))

    args = ap.parse_args(argv)

    logging.basicConfig(format="%(message)s", level=logging.DEBUG if args.verbose else logging.WARNING)
    print(solve(args.datafile))


def test_sample():
    assert solve(open("../sample.txt")) == 12


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
