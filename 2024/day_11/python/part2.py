#!/usr/bin/env python3

import argparse
import logging
import math
import sys
from functools import lru_cache, reduce
from pathlib import Path


def solve(datafile):
    return sum(blink(n, 75) for n in [int(t) for t in datafile.read().split()])


@lru_cache(maxsize=None)
def blink(n, times):
    return (
        1 if times == 0 else sum(blink(r, times - 1) for r in transform_n(n))
    )


def transform_n(n):
    if n == 0:
        return [1]
    if (c := digit_count(n)) % 2 == 0:
        ds = digits(n)
        return [num(ds[: c // 2]), num(ds[c // 2 :])]
    return [n * 2024]


def num(ds):
    return reduce(lambda t, d: t * 10 + d, ds, 0)


def digit_count(n):
    return int(math.log10(n) + 1)


def digits(n):
    result = []
    while n:
        n, r = divmod(n, 10)
        result.append(r)
    result.reverse()
    return result


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


def test_digits():
    assert digits(1) == [1]
    assert digits(11) == [1, 1]
    assert digits(12) == [1, 2]
    assert digits(300) == [3, 0, 0]
    assert digits(304) == [3, 0, 4]


def test_sample2():
    datafile = Path(__file__).parent.parent.joinpath("sample2.txt").open()
    assert solve(datafile) == 65601038650482


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 220357186726677


if __name__ == "__main__":
    main()
