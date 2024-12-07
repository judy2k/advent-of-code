#!/usr/bin/env python3

import argparse
import logging
import sys
from itertools import takewhile
from pathlib import Path


def solve(datafile):
    ordering_rules = set(
        tuple(int(t) for t in line.split("|"))
        for line in takewhile(lambda line: "|" in line, datafile)
    )
    updates = [
        list(int(t) for t in line.split(",")) for line in datafile if "," in line
    ]

    return sum(
        update[len(update) // 2]
        for update in updates
        if all(pair in ordering_rules for pair in zip(update, update[1:]))
    )


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
    assert solve(datafile) == 143


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 5588


if __name__ == "__main__":
    main()
