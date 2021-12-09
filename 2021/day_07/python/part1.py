#!/usr/bin/env python3

import argparse
import logging
import sys


def solve(datafile):
    input = [int(n) for n in datafile.read().split(",")]
    return min(calculate(input, location) for location in input)


def calculate(positions, location):
    return sum(abs(position - location) for position in positions)


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("datafile", type=argparse.FileType(mode="r"))

    args = ap.parse_args(argv)

    logging.basicConfig(
        format="%(message)s", level=logging.DEBUG if args.verbose else logging.WARNING
    )
    print(solve(args.datafile))


def test_sample():
    assert solve(open("../sample.txt")) == 37


if __name__ == "__main__":
    main()
