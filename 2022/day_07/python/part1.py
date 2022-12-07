#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

import re


def parse_datafile(datafile):
    size = 0
    subdirs = []

    for line in (l.strip() for l in datafile):
        if line == "$ cd ..":
            break
        elif line.startswith(r"$ cd"):
            ds = parse_datafile(datafile)
            size += ds[0]
            subdirs.extend(ds)
        elif match := re.match(r"\d+", line):
            size += int(match.group(0))

    return [size] + subdirs


def solve(datafile):
    return sum(n for n in parse_datafile(datafile) if n <= 100_000)


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
    assert solve(sample_file) == 95_437


def test_input():
    from pathlib import Path

    input_file = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(input_file) == 1_423_358


def test_sample_size():
    from pathlib import Path

    input_file = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert parse_datafile(input_file)[0] == 48_381_165


if __name__ == "__main__":
    main()
