#!/usr/bin/env python3

import argparse
import logging
import os
import sys
from pathlib import Path


def solve(datafile):
    or_tuples = [
        tuple(int(t) for t in line.split("|")) for line in datafile if "|" in line
    ]
    datafile.seek(0, os.SEEK_SET)
    pages_to_print = [
        [list(int(t) for t in line.split(",")) for line in datafile if "," in line]
    ]

    return 0


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
import pytest


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 143


@pytest.mark.xfail
def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == -1


if __name__ == "__main__":
    main()
    main()
    main()
