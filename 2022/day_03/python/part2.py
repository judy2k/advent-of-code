#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

from string import ascii_letters

scores = {l: i for i, l in enumerate(ascii_letters, start=1)}


def n(i, c):
    try:
        while True:
            yield [next(i).strip() for _ in range(c)]
    except StopIteration:
        pass


def score_triple(triple):
    return scores[set(triple[0]).intersection(triple[1]).intersection(triple[2]).pop()]


def solve(datafile):
    return sum(score_triple(t) for t in n(datafile, 3))


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("datafile", type=argparse.FileType(mode="r"))

    args = ap.parse_args(argv)

    logging.basicConfig(format="%(message)s", level=logging.DEBUG if args.verbose else logging.WARNING)
    print(solve(args.datafile))


def test_sample():
    assert solve(open("../sample.txt")) == 70
    assert solve(open("../input.txt")) == 2479


if __name__ == "__main__":
    main()
