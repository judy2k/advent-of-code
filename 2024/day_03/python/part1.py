#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import sys

import re

INSTRUCTION_FINDER = re.compile(r"""mul\((\d{1,3}),(\d{1,3})\)""")


def solve(datafile):
    tally = 0
    for a, b in INSTRUCTION_FINDER.findall(datafile.read()):
        tally += int(a) * int(b)

    return tally


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
    assert solve(datafile) == 161


def test_regex():
    match = INSTRUCTION_FINDER.match("mul(12,13)")
    assert match is not None
    assert match.group(1) == "12"
    assert match.group(2) == "13"


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 175015740


if __name__ == "__main__":
    main()
