#!/usr/bin/env python3

import argparse
import logging
import sys
from itertools import permutations
from pathlib import Path


def tsub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def tadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def solve(datafile):
    antennae: dict[str, set[tuple[int, int]]] = {}
    for row, line in enumerate(datafile):
        for col, char in enumerate(line.strip()):
            if char != ".":
                antennae.setdefault(char, set()).add((row, col))

    width = col + 1
    height = row + 1

    antinodes = set()

    def in_bounds(location):
        row, col = location
        return 0 <= row < height and 0 <= col < width

    for locations in antennae.values():
        for a, b in permutations(locations, 2):
            d = tsub(b, a)
            location = a
            while True:
                location = tadd(location, d)
                if in_bounds(location):
                    antinodes.add(location)
                else:
                    break

    return len(antinodes)


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


# Tests ------------------------------------------------------------------------


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 34


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 1131


if __name__ == "__main__":
    main()
