#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

import re


def read_calibrations(datafile):
    for line in datafile:
        digits = re.findall(r"\d", line)
        yield int(digits[0] + digits[-1])


def solve(datafile):
    numbers = read_calibrations(datafile)

    return sum(numbers)


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


from pathlib import Path


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 142


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 54951


if __name__ == "__main__":
    main()
