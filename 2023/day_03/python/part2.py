#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

from dataclasses import dataclass


digits = set(str(i) for i in range(10))
not_symbols = digits | {'.'}


@dataclass
class Number:
    row: int
    startcol: int
    endcol: int
    number: int

    def adjacent(self, row: int, col: int) -> bool:
        if abs(self.row - row) <= 1:
            return self.startcol - 1 <= col <= self.endcol + 1
        return False


def find_numbers(grid):
    for row, line in enumerate(grid):
        col = 0
        while col < len(line):
            char = line[col]
            if char in digits:
                number = [row, col]
                while True:
                    if line[col+1:col+2] in digits:
                        col += 1
                    else:
                        break
                number.append(col)
                number.append(int(line[number[1]:number[2] + 1]))
                debug("Added number: %d", int(line[number[1]:number[2] + 1]))
                yield Number(*number) #row, startcol, endcol, value
            col += 1


def find_gears(grid):
    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            if char == '*':
                yield (row, col)


def solve(datafile):
    grid = [line.strip() for line in datafile.readlines()]
    tally = 0
    numbers = list(find_numbers(grid))
    for row, col in find_gears(grid):
        adjacent = list(filter(lambda n: n.adjacent(row, col), numbers))
        if len(adjacent) == 2:
            tally += adjacent[0].number * adjacent[1].number
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
    print(f"Result: {solve(args.datafile)}")


from pathlib import Path


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 467835


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 84907174


if __name__ == "__main__":
    main()
