#!/usr/bin/env python3

import argparse
import logging
import math
import sys
from pathlib import Path


def solve(datafile):
    ns = [int(t) for t in datafile.read().split()]
    print(" ".join(str(n) for n in ns))

    for step in range(25):
        ns = list(blink(ns))
        print(ns)

    return len(ns)


def blink(ns):
    for n in ns:
        if n == 0:
            yield 1
        elif (c := digit_count(n)) % 2 == 0:
            ds = digits(n)
            yield num(ds[: c // 2])
            yield num(ds[c // 2 :])
        else:
            yield n * 2024


def num(ds):
    result = 0
    for d in ds:
        result = result * 10 + d
    return result


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


# def test_sample1():
#     datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
#     assert solve(datafile) == TODO


def test_digits():
    assert digits(1) == [1]
    assert digits(11) == [1, 1]
    assert digits(12) == [1, 2]
    assert digits(300) == [3, 0, 0]
    assert digits(304) == [3, 0, 4]


def test_sample2():
    datafile = Path(__file__).parent.parent.joinpath("sample2.txt").open()
    assert solve(datafile) == 55312


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 184927


if __name__ == "__main__":
    main()
