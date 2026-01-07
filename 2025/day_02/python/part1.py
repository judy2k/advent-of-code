#!/usr/bin/env python3

import argparse
import logging
from logging import info
import re
import sys
from pathlib import Path
from typing import Any, Generator

import pytest

def parse_ranges(s: str) -> Generator[range, Any, None]:
    return (range(int(match.group(1)),int(match.group(2)) + 1) for match in re.finditer(r'(\d+)-(\d+)', s))


def is_invalid(s: str):
    l = len(s)
    return s[:l//2] == s[l//2:]


def solve(datafile):
    tally = 0
    for r in parse_ranges(datafile.read()):
        for i in r:
            if is_invalid(str(i)):
                tally += i

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

def test_is_invalid():
    assert is_invalid("11")
    assert not is_invalid("12")
    assert is_invalid("22")
    assert is_invalid("1010")
    assert not is_invalid("1011")
    assert is_invalid("38593859")
    assert not is_invalid("38593860")

def test_parse_ranges():
    assert list(parse_ranges("1-3,2-7")) == [range(1,4), range(2,8)]

def test_sample():
    info("Loading sample")
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 1227775554

def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 5398419778


if __name__ == "__main__":
    main()
