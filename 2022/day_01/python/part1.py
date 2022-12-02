#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

from itertools import takewhile


def parse_lines(datafile):
    return (int(line) if line.strip() else None for line in datafile)


def group(items):
    while True:
        group = list(takewhile(lambda x: x is not None, items))
        if group:
            yield sum(group)
        else:
            break


def solve(datafile):
    items = group(parse_lines(datafile))
    return max(items)


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("datafile", type=argparse.FileType(mode="r"))

    args = ap.parse_args(argv)

    logging.basicConfig(format="%(message)s", level=logging.DEBUG if args.verbose else logging.WARNING)
    print(solve(args.datafile))


def test_sample():
    assert solve(open("../sample.txt")) == 24000


if __name__ == "__main__":
    main()
