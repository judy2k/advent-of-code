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
    stack_rows = []
    for line in datafile:
        if line.startswith(" 1"):
            datafile.readline()
            break
        stack_rows.append(line.strip("\n")[1::4])

    stacks = [list(takewhile(lambda s: s != " ", stack)) for stack in list(zip(*reversed(stack_rows)))]

    return stacks


def parse_moves(datafile):
    for line in datafile:
        if m := re.match(r"move (\d+) from (\d+) to (\d+)", line):
            yield Move(*(int(s) for s in m.groups()))


def solve(datafile):
    stacks = parse_stacks(datafile)
    moves = list(parse_moves(datafile))

    for move in moves:
        info(move)
        debug(f"From: {stacks[move.source - 1]}, To: {stacks[move.to - 1]}")
        stacks[move.to - 1].extend(stacks[move.source - 1][-move.count :])
        del stacks[move.source - 1][-move.count :]
        debug(f"After:{stacks[move.source - 1]}, {stacks[move.to - 1]}")

    return "".join(stack[-1] if stack else "" for stack in stacks)


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("datafile", type=argparse.FileType(mode="r"))

    args = ap.parse_args(argv)

    logging.basicConfig(format="%(message)s", level=logging.DEBUG if args.verbose else logging.WARNING)
    print(solve(args.datafile))


def test_sample():
    assert solve(open("../sample.txt")) == "MCD"


def test_parse_stacks():
    assert parse_stacks(open("../sample.txt")) == [["Z", "N"], ["M", "C", "D"], ["P"]]


if __name__ == "__main__":
    main()
