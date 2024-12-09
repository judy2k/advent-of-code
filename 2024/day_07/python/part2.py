#!/usr/bin/env python3

import argparse
import logging
import math
import sys
from collections import deque
from itertools import product
from operator import add, mul
from pathlib import Path


def append(a, b):
    return a * (10 ** (int(math.log10(b)) + 1)) + b


def is_solvable(target, operands):
    possible_operators = [add, mul, append]
    combos = product(possible_operators, repeat=len(operands) - 1)

    for operators in combos:
        stack = deque(operands)
        for operator in operators:
            stack.appendleft(operator(stack.popleft(), stack.popleft()))
        if stack.popleft() == target:
            return True
    return False


def parse_line(line):
    target, operands = line.split(": ")
    target = int(target)
    operands = [int(t) for t in operands.split()]

    return target, operands


def solve(datafile):
    return sum(
        target
        for target, operands in (parse_line(line) for line in datafile)
        if is_solvable(target, operands)
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
    assert solve(datafile) == 11387


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 116094961956019


def test_append():
    assert append(1, 2) == 12
    assert append(10, 2) == 102
    assert append(123, 45) == 12345


if __name__ == "__main__":
    main()
