#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

import pytest

from itertools import *


def n_wise(iterable, n=4):
    return zip(*(islice(c, i, None) for i, c in enumerate(tee(iterable, n))))


def solve(datafile):
    ns = n_wise(datafile.read())
    for i, n in enumerate(ns):
        debug("%d: %s", i, n)
        if len(set(n)) == 4:
            return i + 4

    return 0


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
    assert solve(open("../sample.txt")) == 7


def test_n_wise():
    r = range(1, 7)
    ns = n_wise(r)
    assert next(ns) == (1, 2, 3, 4)
    assert next(ns) == (2, 3, 4, 5)
    assert next(ns) == (3, 4, 5, 6)
    with pytest.raises(StopIteration):
        next(ns)


def test_n_wise_infinite():
    r = count()
    ns = n_wise(r)
    assert next(ns) == (0, 1, 2, 3)
    assert next(ns) == (1, 2, 3, 4)
    assert next(ns) == (2, 3, 4, 5)
    assert next(ns) == (3, 4, 5, 6)


if __name__ == "__main__":
    main()
