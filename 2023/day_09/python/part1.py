#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import sys

import re

def numbers(line):
    return [int(s) for s in re.findall(r'-?\d+', line)]


def solve(datafile):
    for line in datafile:
        ns = numbers(line)

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

# Tests ------------------------------------------------------------------------

def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 114


# def test_input():
#     datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
#     assert solve(datafile) == TODO


if __name__ == "__main__":
    main()
