#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import sys

import re


def parse_line(line):
    return (
        set(int(s) for s in re.split(r" +", ns.strip()))
        for ns in re.match(r"Card +\d+: ([^|]*) \| +(.*)", line).group(1, 2)
    )
    

def solve(datafile):
    scores = []
    for line in datafile:
        winning, owned = parse_line(line)
        scores.append(len(winning & owned))

    counts = [1 for _ in scores]
    for current, score in enumerate(scores):
        for n in range(current + 1, current + score + 1):
            counts[n] += counts[current]

    return sum(counts)


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
    assert solve(datafile) == 30


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 23806951


if __name__ == "__main__":
    main()
