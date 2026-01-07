#!/usr/bin/env python3

import argparse
import logging
import sys
from itertools import takewhile
from pathlib import Path
from typing import IO


def parse_range(s: str) -> range:
    start, stop = map(int, s.strip().split('-'))
    return range(start, stop+1)


def parse_file(datafile: IO[str]) -> tuple[list[range], list[int]]:
    ranges = [parse_range(line) for line in takewhile(lambda l: l.strip(), datafile)]
    ids = [int(line.strip()) for line in datafile]
    return ranges, ids


def solve(datafile):
    ranges, ids = parse_file(datafile)
    return len(set(i for r in ranges for i in ids if i in r))


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

def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 3


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 726


if __name__ == "__main__":
    main()
