#!/usr/bin/env python3

import argparse
import itertools
import logging
import re
import sys
from pathlib import Path


def solve(datafile):
    tally = 0
    input_lines = [line.strip() for line in datafile.readlines()]
    for line in all_lines(input_lines):
        tally += len(re.findall("XMAS", line))

    return tally


def all_lines(input_lines):
    return and_reversed(
        itertools.chain(
            [line for line in input_lines],
            ["".join(col) for col in (zip(*input_lines))],
            ["".join(col) for col in (diagonal(input_lines))],
            [
                "".join(col)
                for col in reversed(list(diagonal(list(reversed(input_lines)))))
            ],
        )
    )


def and_reversed(inputs):
    for input in inputs:
        yield input
        yield "".join(reversed(input))


def diagonal(input_lines):
    line_len = len(input_lines[0])
    for start_x in range(line_len - 1, 0, -1):
        line = []
        x, y = start_x, 0
        while x < line_len and y < len(input_lines):
            line.append(input_lines[y][x])
            x += 1
            y += 1
        yield "".join(line)

    for start_y in range(len(input_lines)):
        line = []
        x, y = 0, start_y
        while x < line_len and y < len(input_lines):
            line.append(input_lines[y][x])
            x += 1
            y += 1
        yield "".join(line)


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


def test_all_lines():
    input_lines = [
        line.strip()
        for line in """abc
def
ghi""".splitlines()
    ]
    assert list(all_lines(input_lines)) == [
        # Horizontal:
        "abc",
        "cba",
        "def",
        "fed",
        "ghi",
        "ihg",
        # Vertical:
        "adg",
        "gda",
        "beh",
        "heb",
        "cfi",
        "ifc",
        # Diagonals, down to the right:
        "c",
        "c",
        "bf",
        "fb",
        "aei",
        "iea",
        "dh",
        "hd",
        "g",
        "g",
        # Diagonals, up to the right:
        "a",
        "a",
        "db",
        "bd",
        "gec",
        "ceg",
        "hf",
        "fh",
        "i",
        "i",
    ]


if __name__ == "__main__":
    main()
