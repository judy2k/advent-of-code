#!/usr/bin/env python3

import argparse
import logging
import re
import sys
from pathlib import Path

INSTRUCTION_FINDER = re.compile(r"""mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)""")


def solve(datafile):
    active = True
    tally = 0
    for inst in INSTRUCTION_FINDER.finditer(datafile.read()):
        s = inst.group()
        if s == "do()":
            active = True
        elif s == "don't()":
            active = False
        elif active and s.startswith("mul"):
            a, b = inst.groups()
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
    assert solve(datafile) == 112272912


if __name__ == "__main__":
    main()
