#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import sys

from functools import reduce
from itertools import product, repeat
from operator import __mul__


def takeuntil(predicate, iterable):
    for x in iterable:
        yield x
        if predicate(x):
            break


def score(map, cx, cy):
    h = map[cy][cx]

    ranges = [
        zip(repeat(cx), reversed(range(0, cy))),
        zip(repeat(cx), range(cy + 1, len(map))),
        zip(range(cx + 1, len(map[0])), repeat(cy)),
        zip(reversed(range(0, cx)), repeat(cy)),
    ]

    result = reduce(
        __mul__,
        (
            sum(
                1
                for _ in takeuntil(lambda n: n >= h, (map[y][x] for x, y in r))
            )
            for r in ranges
        ),
        1,
    )

    return result


def solve(datafile):
    map = [[int(c) for c in line.strip()] for line in datafile]

    return max(
        score(map, x, y)
        for x, y in product(range(len(map[0])), range(len(map)))
    )


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


def test_sample():
    sample_file = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(sample_file) == 8


def test_input():
    input_file = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(input_file) == 444528


def test_score():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    map = [[int(c) for c in line.strip()] for line in datafile]

    assert score(map, 2, 1) == 4
    assert score(map, 2, 3) == 8


if __name__ == "__main__":
    main()
