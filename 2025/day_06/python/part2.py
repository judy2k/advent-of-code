#!/usr/bin/env python3

import argparse
import logging
import operator
import sys
from functools import reduce
from itertools import zip_longest
from pathlib import Path
from typing import IO, Sequence


class Calc:
    def __init__(self):
        self.operands = []
        self.operator = None

    def solve(self) -> int:
        return operations[self.operator](self.operands)

    def __repr__(self):
        return f"({self.operator} {self.operands})"


def add(operands: Sequence[int]) -> int:
    return reduce(operator.add, operands, 0)


def mul(operands: Sequence[int]) -> int:
    return reduce(operator.mul, operands, 1)


operations = {
    '+': add,
    '*': mul,
}


def parse(datafile: IO[str]):
    rows = [reversed(line.strip('\n')) for line in datafile]
    cols = [''.join(col) for col in zip(*rows)]

    calc = Calc()
    for col in cols:
        if col.strip():
            calc.operands.append(int(col[:-1]))
            if col[-1] != ' ':
                calc.operator = col[-1]
                yield calc
                calc = Calc()



def solve(datafile):
    return sum(calc.solve() for calc in parse(datafile))


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
    assert solve(datafile) == 3263827


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == -1


if __name__ == "__main__":
    main()
