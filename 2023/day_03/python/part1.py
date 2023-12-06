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


def symbols(grid):
    return set(''.join(grid)) - not_symbols

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

def adjacent_char(number, grid, symbols):
    row, startcol, endcol = number.row, number.startcol, number.endcol
    surrounding_chars = set()
    if row > 0:
        above = grid[row - 1][max(startcol - 1, 0): endcol + 2]
        surrounding_chars |= set(above)
    if startcol > 0:
        before = grid[row][startcol - 1]
        surrounding_chars |= set(before)
    if endcol < len(grid[0]) - 1:
        after = grid[row][endcol + 1]
        surrounding_chars |= set(after)
    if row < len(grid) - 1:
        below = grid[row + 1][max(startcol - 1, 0): endcol + 2]
        surrounding_chars |= set(below)
    if surrounding_chars & symbols:
        return True
    

def solve(datafile):
    grid = [line.strip() for line in datafile.readlines()]
    schars = symbols(grid)
    return sum( number.number for number in find_numbers(grid) if adjacent_char(number, grid, schars))


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
    assert solve(datafile) == 4361


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 528799


if __name__ == "__main__":
    main()
