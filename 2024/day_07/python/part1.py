#!/usr/bin/env python3

import argparse
import logging
import sys
from collections import deque
from itertools import product
from operator import add, mul
from pathlib import Path


def is_solvable(target, operands):
    possible_operators = [add, mul]
    combos = product(possible_operators, repeat=len(operands) - 1)

    for operators in combos:
        stack = deque(operands)
        for operator in operators:
            stack.appendleft(operator(stack.popleft(), stack.popleft()))
        if stack.popleft() == target:
            return True
    return False


def solve(datafile):
    tally = 0

    for line in datafile:
        target, operands = line.split(": ")
        target = int(target)
        operands = [int(t) for t in operands.split()]

        if is_solvable(target, operands):
            tally += target

    return tally


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
    assert solve(datafile) == 3749


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 267566105056


if __name__ == "__main__":
    main()
