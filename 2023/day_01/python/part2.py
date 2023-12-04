#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

import re

mapping = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    **{str(k): str(k) for k in range(1, 10)},
}
regex = re.compile(f"(?=({'|'.join(mapping.keys())}))")


def read_calibrations(datafile):
    for line in datafile:
        digits = regex.findall(line)
        print(
            line.strip(),
            "|",
            digits[0],
            digits[-1],
            "|",
            mapping[digits[0]],
            mapping[digits[-1]],
            "|",
            int(mapping[digits[0]] + mapping[digits[-1]]),
        )
        yield int(mapping[digits[0]] + mapping[digits[-1]])


def solve(datafile):
    numbers = read_calibrations(datafile)

    return sum(numbers)


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


from pathlib import Path
from pytest import fail


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample2.txt").open()
    assert solve(datafile) == 281


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) > 55189


def test_edge():
    assert regex.findall("oneightwone") == ["one", "eight", "two", "one"]


if __name__ == "__main__":
    main()
