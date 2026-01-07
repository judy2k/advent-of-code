#!/usr/bin/env python3

import argparse
import logging
import sys
from itertools import count
from pathlib import Path
from typing import Any, Generator, IO, Sequence, Iterable, Iterator


def joltage_digits(digit_list: list[int], d: int) -> Iterator[int]:
    """ Generate the joltage digit sequence from a list of digits. """
    start = 0
    for remaining_digits in reversed(range(d)):
        digit = max(digit_list[start:-remaining_digits or None])
        start = digit_list.index(digit, start) + 1
        yield digit


def joltage(digits: list[int], d: int) -> int:
    """ Calculate the total joltage value for a given list of digits. """
    return decimal(joltage_digits(digits, d), d)


def solve(datafile: IO[str]) -> int:
    """ Solve the puzzle. """
    return sum(joltage(digits(line), 12) for line in datafile)


def digits(s: str) -> list[int]:
    """ Convert a string to a list of its digits, as integers. """
    return [int(c) for c in s.strip()]


def decimal(ns: Iterator[int], ns_len: int) -> int:
    """ Convert a sequence of digits, as integers, to a decimal number. """
    return sum(i * (10 ** e) for i, e in zip(ns, count(ns_len - 1, -1)))


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
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


def test_joltage():
    assert joltage(digits('987654321111111'), 2) == 98
    assert joltage(digits('811111111111119'), 2) == 89
    assert joltage(digits('234234234234278'), 2) == 78
    assert joltage(digits('818181911112111'), 2) == 92

def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 3121910778619


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 168627047606506


if __name__ == "__main__":
    main()
