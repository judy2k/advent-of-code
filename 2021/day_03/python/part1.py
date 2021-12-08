#!/usr/bin/env python3

import argparse
from collections import Counter
from operator import mul
import logging
import sys


def solve(datafile):
    values = [line.strip() for line in datafile.readlines()]
    counters = [Counter(col) for col in zip(*values)]

    gamma, epsilon = (bits_to_int(s) for s in zip(*map(most_common_keys, counters)))

    return gamma * epsilon


def most_common_keys(counter):
    return tuple(k for k, v in counter.most_common())


def bits_to_int(bits):
    return int("".join(bits), 2)


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("datafile", type=argparse.FileType(mode="r"))

    args = ap.parse_args(argv)

    logging.basicConfig(
        format="%(message)s", level=logging.DEBUG if args.verbose else logging.WARNING
    )
    print(solve(args.datafile))


def test_sample():
    assert solve(open("../sample.txt")) == 198


if __name__ == "__main__":
    main()
