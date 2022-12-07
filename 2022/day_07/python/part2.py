#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

import re


def parse_datafile(datafile):
    directories = []
    stack = []

    for line in datafile:
        if line.strip() == "$ cd ..":
            directories[stack[-2]] += directories[stack.pop()]
        elif match := re.match(r"\$ cd (.*)", line.strip()):
            stack.append(len(directories))
            directories.append(0)
        elif match := re.match(r"(?P<size>\d+) (?:\w+)", line.strip()):
            directories[stack[-1]] += int(match.group("size"))
    while len(stack) > 1:
        directories[stack[-2]] += directories[stack.pop()]

    return directories


def solve(datafile):
    ds = parse_datafile(datafile)
    return sorted((d for d in ds if d >= 30_000_000 - (70_000_000 - ds[0])))[0]


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
    from pathlib import Path

    sample_file = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(sample_file) == 24933642


def test_input():
    from pathlib import Path

    input_file = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(input_file) == 545729


if __name__ == "__main__":
    main()
