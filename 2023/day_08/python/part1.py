#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import sys

from itertools import cycle
import re


def parse_file(datafile):
    instructions = cycle(iter(datafile.readline().strip()))
    datafile.readline() #skip

    tree = {}
    for line in datafile:
        if m := re.match(r'(\w+) = \((\w+), (\w+)\)', line.strip()):
            k, l, r = m.groups()
            tree[k] = (l, r)
        else:
            raise Exception(f"Unknown map line: {line}")
    
    return instructions, tree


def solve(datafile):
    instructions, tree = parse_file(datafile)
    
    steps = 0
    pos = 'AAA'
    while pos != 'ZZZ':
        i = next(instructions)
        steps += 1
        if i == 'L':
            pos = tree[pos][0]
        elif i == 'R':
            pos = tree[pos][1]
        else:
            raise Exception(f"Unknown instruction {i}")

    return steps


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
    assert solve(datafile) == 2


def test_sample2():
    datafile = Path(__file__).parent.parent.joinpath("sample2.txt").open()
    assert solve(datafile) == 6


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 19241


if __name__ == "__main__":
    main()
