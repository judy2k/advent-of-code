#!/usr/bin/env python3

import argparse
import logging
import sys
from pathlib import Path

XMAS = list("XMAS")


def solve(datafile):
    tally = 0
    input_lines: list[list[str]] = [list(line.strip()) for line in datafile.readlines()]

    row_count = len(input_lines)
    col_count = len(input_lines[0])

    for row in range(row_count):
        for col in range(col_count):
            if input_lines[row][col] == "X":
                tally += sum(
                    1
                    for slice in (
                        input_lines[row][col : col + 4],
                        input_lines[row][col : col - 4 if col >= 4 else None : -1],
                        [
                            input_lines[r][col]
                            for r in range(row, min(row_count, row + 4))
                        ],
                        [
                            input_lines[r][col]
                            for r in range(row, row - 4 if row >= 4 else -1, -1)
                        ],
                        [
                            input_lines[row + i][col + i]
                            for i in range(4)
                            if row + i < row_count and col + i < col_count
                        ],
                        [
                            input_lines[row - i][col - i]
                            for i in range(4)
                            if row - i >= 0 and col - i >= 0
                        ],
                        [
                            input_lines[row + i][col - i]
                            for i in range(4)
                            if row + i < row_count and col - i >= 0
                        ],
                        [
                            input_lines[row - i][col + i]
                            for i in range(4)
                            if row - i >= 0 and col + i < col_count
                        ],
                    )
                    if slice == XMAS
                )

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
    assert solve(datafile) == 18


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 2483


if __name__ == "__main__":
    main()
