#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import sys

from bisect import bisect_right
import re
from operator import itemgetter


class Mapping:
    def __init__(self, ranges):
        self.starts = [0]
        self.offsets = [0]

        for d, s, n in sorted(ranges, key=itemgetter(1)):
            if s == self.starts[-1]:
                self.offsets[-1] = d - s
                self.starts.append(s + n)
                self.offsets.append(0)
            else:
                self.starts.append(s)
                self.offsets.append(d - s)
                self.starts.append(s + n)
                self.offsets.append(0)

    def map(self, val):
        i = bisect_right(self.starts, val) - 1
        return val + self.offsets[i]


def numbers(s):
    return tuple([int(i) for i in re.findall(r"-?\d+", s)])


def map_all(mappings, val):
    for mapping in mappings:
        val = mapping.map(val)
    return val


def parse_file(datafile):
    seeds = numbers(datafile.readline().split(":")[1])
    maps = []

    assert datafile.readline() == "\n"

    map_from, map_to = None, None
    mapping_tuples = []
    while True:
        # Read mapping:
        line = datafile.readline()
        if match := re.match(r"(\w+)-to-(\w+) map:", line):
            map_from, map_to = match.groups()
        elif line in {"", "\n"}:
            maps.append(Mapping(mapping_tuples))

            map_from, map_to = None, None
            mapping_tuples = []
            if not line:
                break  # eof
        else:
            d, s, n = numbers(line)
            mapping_tuples.append((d, s, n))

    return seeds, maps


def solve(datafile):
    seeds, maps = parse_file(datafile)
    return min(map_all(maps, seed) for seed in seeds)


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


def test_parse_file():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    seeds, maps = parse_file(datafile)
    assert seeds == (79, 14, 55, 13)
    m = maps[0]
    assert m.map(79) == 81
    assert m.map(14) == 14
    assert m.map(55) == 57
    assert m.map(13) == 13


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 35


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 240320250


def test_bisect():
    o = [0, 4, 7]
    assert bisect_right(o, 0) - 1 == 0
    assert bisect_right(o, 1) - 1 == 0
    assert bisect_right(o, 3) - 1 == 0
    assert bisect_right(o, 4) - 1 == 1
    assert bisect_right(o, 5) - 1 == 1
    assert bisect_right(o, 7) - 1 == 2
    assert bisect_right(o, 8) - 1 == 2


if __name__ == "__main__":
    main()
