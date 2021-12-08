#!/usr/bin/env python3

import argparse
from itertools import tee, islice, count
import logging
import sys


def solve(datafile):
    ints = (int(line) for line in datafile)
    return sum(sum(i) < sum(j) for i, j in rolling_window(rolling_window(ints, 3), 2))


def rolling_window(iterator, n):
    return zip(*(islice(it, i, None) for (i, it) in enumerate(tee(iterator, n))))


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("datafile", type=argparse.FileType(mode="r"))

    args = ap.parse_args(argv)

    logging.basicConfig(
        format="%(message)s", level=logging.DEBUG if args.verbose else logging.WARNING
    )
    print(solve(args.datafile))


def test_rolling_window():
    assert list(rolling_window(range(5), 2)) == [(0, 1), (1, 2), (2, 3), (3, 4)]
    i = rolling_window(count(), 2)
    assert next(i) == (0, 1)
    assert next(i) == (1, 2)
    i = rolling_window(count(), 1_000)
    assert next(i) == tuple(range(1_000))
    assert list(rolling_window([], 0)) == []
    assert list(rolling_window([], 5)) == []
    assert list(rolling_window(range(5), 3)) == [(0, 1, 2), (1, 2, 3), (2, 3, 4)]


def test_sample():
    assert solve(open("../sample.txt")) == 5


if __name__ == "__main__":
    main()
