#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys


SCORES = {
    "A X": 1 + 3,
    "A Y": 2 + 6,
    "A Z": 3 + 0,
    "B X": 1 + 0,
    "B Y": 2 + 3,
    "B Z": 3 + 6,
    "C X": 1 + 6,
    "C Y": 2 + 0,
    "C Z": 3 + 3,
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
