#!/usr/bin/env python3

import argparse
import logging
from math import floor
import sys


def calculate_fuel(weight):
    if (new_weight := floor(int(weight) / 3.0) - 2) <= 0:
        return 0
    return new_weight + calculate_fuel(new_weight)


def solve(datafile):
    return sum(calculate_fuel(int(line)) for line in datafile)


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("datafile", type=argparse.FileType(mode="r"))

    args = ap.parse_args(argv)
    print(solve(args.datafile))


if __name__ == "__main__":
    main()
