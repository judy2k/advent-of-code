#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

import math
import re
from string import ascii_uppercase


def parse_stacks(datafile):
    stack_rows = []
    for line in datafile:
        if line.startswith(" 1"):
            break
        else:
            stack_rows.append(line.strip("\n"))

    stack_count = int(math.ceil(len(stack_rows[0]) / 4))
    stacks = [[] for _ in range(stack_count)]
    for row in reversed(stack_rows):
        for i in range(stack_count):
            letter = row[i * 4 + 1]
            if letter in ascii_uppercase:
                stacks[i].append(letter)

    return stacks


def solve(datafile):

    return 0


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
