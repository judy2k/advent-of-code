#!/usr/bin/env python3

import argparse
import itertools
import logging
import sys
from pathlib import Path

DIAGONALS = {
    tuple("MAS"),
    tuple("SAM"),
}


def solve(datafile):
    tally = 0
    input_lines: list[list[str]] = [list(line.strip()) for line in datafile.readlines()]

    row_count = len(input_lines)
    col_count = len(input_lines[0])

    def chars(f):
        return (
            input_lines[row][col]
            for row, col in (f(i) for i in range(3))
            if 0 <= row < row_count and 0 <= col < col_count
        )

    for row, col in itertools.product(range(row_count), range(col_count)):
        if input_lines[row][col] == "A":
            if (
                tuple(chars(lambda i: (row - 1 + i, col - 1 + i))) in DIAGONALS
                and tuple(chars(lambda i: (row + 1 - i, col - 1 + i))) in DIAGONALS
            ):
                tally += 1

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
    assert solve(datafile) == 9


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 1925


if __name__ == "__main__":
    main()
