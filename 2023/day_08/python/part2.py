#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import sys

from itertools import cycle
from math import lcm
import re


def parse_file(datafile):
    instructions = datafile.readline().strip()
    datafile.readline()  # skip line

    tree = {}
    for line in datafile:
        if m := re.match(r"(\w+) = \((\w+), (\w+)\)", line.strip()):
            k, l, r = m.groups()
            tree[k] = (l, r)
        else:
            raise Exception(f"Unknown map line: {line}")

    return instructions, tree


def solve(datafile):
    instructions, tree = parse_file(datafile)
    instructions = cycle(0 if c == "L" else 1 for c in instructions)
    pos = [n for n in tree if n.endswith("A")]
    steps = 0
    repeats = {}
    while len(repeats) < len(pos):
        instruction = next(instructions)
        steps += 1

        pos = [tree[p][instruction] for p in pos]

        for i, p in enumerate(pos):
            if p.endswith("Z"):
                repeats.setdefault(i, steps)

    return lcm(*repeats.values())


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


def test_sample3():
    datafile = Path(__file__).parent.parent.joinpath("sample3.txt").open()
    assert solve(datafile) == 6


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 9606140307013


if __name__ == "__main__":
    main()
