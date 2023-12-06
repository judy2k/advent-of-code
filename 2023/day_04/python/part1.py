#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import sys

import re


def parse_line(line):
    card, numbers = line.strip().split(": ")
    winning, owned = numbers.split("|")
    winning, owned = [
        set(int(s) for s in re.split(r" +", ns.strip())) for ns in (winning, owned)
    ]
    return card, winning, owned


def solve(datafile):
    tally = 0
    for line in datafile:
        _, winning, owned = parse_line(line)
        matches = winning & owned
        if matches:
            tally += 2 ** (len(matches) - 1)

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
    assert solve(datafile) == 13


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 20407


if __name__ == "__main__":
    main()
