#!/usr/bin/env python3

import argparse
import logging
from logging import warning
import sys
from itertools import takewhile
from pathlib import Path
from typing import IO

from tqdm import tqdm


def parse_range(s: str) -> range:
    start, stop = map(int, s.strip().split('-'))
    return range(start, stop+1)


def parse_file(datafile: IO[str]) -> tuple[list[range], list[int]]:
    ranges = [parse_range(line) for line in takewhile(lambda l: l.strip(), datafile)]
    ids = [int(line.strip()) for line in datafile]
    return ranges, ids


def merge_ranges(ranges: list[range]):
    sorted_ranges = sorted(ranges, key=lambda r: r.start)
    result = []

    i = 0
    while i < len(sorted_ranges):
        left = sorted_ranges[i]
        for j in range(i+1, len(sorted_ranges)):
            right = sorted_ranges[j]
            if left.stop >= right.start:
                left = range(left.start, max(left.stop, right.stop))
                i = j+1
            else:
                i = j
                break
        result.append(left)

    return result


def solve(datafile):
    ranges, _ = parse_file(datafile)
    return sum(len(r) for r in merge_ranges(ranges))


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
    assert solve(datafile) == 14


def test_merge_ranges():
    ranges = [range(3, 6), range(10, 15), range(16, 21), range(12, 19)]
    ranges = merge_ranges(ranges)
    assert ranges == [range(3, 6), range(10, 21)]


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 354226555270043


if __name__ == "__main__":
    main()
