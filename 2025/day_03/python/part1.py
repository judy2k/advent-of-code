#!/usr/bin/env python3

import argparse
import logging
import sys
from pathlib import Path

import pytest


def joltage(s: str):
    digits = [int(c) for c in s]
    max_ten = max(digits[:-1])
    unit = max(digits[digits.index(max_ten) + 1:])
    return max_ten * 10 + unit


def solve(datafile):
    return sum(joltage(line.strip()) for line in datafile)


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


def test_joltage():
    assert joltage('987654321111111') == 98
    assert joltage('811111111111119') == 89
    assert joltage('234234234234278') == 78
    assert joltage('818181911112111') == 92

def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 357


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 16946


if __name__ == "__main__":
    main()
