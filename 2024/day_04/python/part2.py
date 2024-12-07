#!/usr/bin/env python3

import argparse
import logging
import sys
from pathlib import Path

MAS = tuple("MAS")
SAM = tuple("SAM")


def solve(datafile):
    tally = 0
    input_lines: list[list[str]] = [list(line.strip()) for line in datafile.readlines()]

    row_count = len(input_lines)
    col_count = len(input_lines[0])

    for row in range(row_count):
        for col in range(col_count):
            if input_lines[row][col] == "A":
                if tuple(
                    input_lines[row - 1 + i][col - 1 + i]
                    for i in range(3)
                    if 0 <= (row - 1 + i) < row_count and 0 <= (col - 1 + i) < col_count
                ) in {MAS, SAM} and tuple(
                    input_lines[row + 1 - i][col - 1 + i]
                    for i in range(3)
                    if 0 <= (row + 1 - i) < row_count and 0 <= (col - 1 + i) < col_count
                ) in {
                    MAS,
                    SAM,
                }:
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
