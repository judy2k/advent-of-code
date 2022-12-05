#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

from collections import namedtuple
from itertools import takewhile
import re


Move = namedtuple("Move", ["count", "source", "to"])


def parse_stacks(datafile):
    return [
        list(takewhile(lambda s: s != " ", stack))
        for stack in zip(
            *reversed(list(takewhile(lambda r: r[0] != "1", (line.strip("\n")[1::4] for line in datafile))))
        )
    ]


def parse_moves(datafile):
    for line in datafile:
        if m := re.match(r"move (\d+) from (\d+) to (\d+)", line):
            yield Move(*(int(s) for s in m.groups()))


def solve(datafile):
    stacks = parse_stacks(datafile)

    for move in parse_moves(datafile):
        for _ in range(move.count):
            stacks[move.to - 1].append(stacks[move.source - 1].pop())

    return "".join(stack[-1] for stack in stacks)


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("datafile", type=argparse.FileType(mode="r"))

    args = ap.parse_args(argv)

    logging.basicConfig(format="%(message)s", level=logging.DEBUG if args.verbose else logging.WARNING)
    print(solve(args.datafile))


def test_sample():
    assert solve(open("../sample.txt")) == "CMZ"


def test_parse_stacks():
    assert parse_stacks(open("../sample.txt")) == [["Z", "N"], ["M", "C", "D"], ["P"]]


if __name__ == "__main__":
    main()
