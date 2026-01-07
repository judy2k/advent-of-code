#!/usr/bin/env python3

import argparse
import logging
import sys
from pathlib import Path

import pytest


def pointings(instructions):
    points_at = 50
    for instruction in instructions:
        direction = instruction[0]
        angle = int(instruction[1:])
        if direction == 'R':
            rem = angle - (100 - points_at)
        else:
            rem = angle - (points_at or 100)
        clicks = 0 if rem < 0 else 1 + (rem // 100)

        points_at = (points_at + (angle if instruction[0] == 'R' else -angle)) % 100
        yield clicks


def solve(datafile):
    return sum(filter(None, pointings(line.strip() for line in datafile)))


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
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
    assert solve(datafile) == 6

def test_to_zero():
    assert solve(['R50']) == 1
    assert solve(['L50']) == 1
    assert solve(['R150']) == 2
    assert solve(['L150']) == 2

def test_crosses_zero():
    assert solve(['R51']) == 1
    assert solve(['L51']) == 1

def test_multiple_rotations():
    assert solve(['R1000']) == 10

def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 6223


if __name__ == "__main__":
    main()
