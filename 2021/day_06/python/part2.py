#!/usr/bin/env python3

import argparse
import logging
import sys

from collections import Counter


def solve(datafile, days=256):
    input = [int(n) for n in datafile.read().split(",")]

    fish = Counter(input)
    for day in range(days):
        fish = step(fish)
    return sum(fish.values())


def step(fish):
    fish = Counter({timer - 1: count for timer, count in fish.items()})
    fish[8] = fish.get(-1, 0)
    fish[6] += fish.pop(-1, 0)
    return fish


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
    assert solve(open("../sample.txt")) == 26984457539


if __name__ == "__main__":
    main()
