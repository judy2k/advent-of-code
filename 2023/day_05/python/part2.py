#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import sys
from typing import List

from bisect import bisect_right
import re
from operator import itemgetter, attrgetter


class Mapping:
    def __init__(self, ranges):
        self.starts = [0]
        self.offsets = [0]

        for d, s, n in sorted(ranges, key=itemgetter(1)):
            if s == self.starts[-1]:
                self.offsets[-1] = d - s
            else:
                self.starts.append(s)
                self.offsets.append(d - s)
            self.starts.append(s + n)
            self.offsets.append(0)

    def map(self, val) -> (int, int):
        i = bisect_right(self.starts, val) - 1
        nextinc = (
            (self.starts[i + 1] - val) if len(self.starts) > i + 1 else sys.maxsize
        )

        return val + self.offsets[i], nextinc


def pairs(l):
    return zip(l[::2], l[1::2])


def numbers(s):
    return tuple([int(i) for i in re.findall(r"\d+", s)])


def map_all(mappings, val) -> (int, int):
    nextinc = sys.maxsize
    for mapping in mappings:
        val, ni = mapping.map(val)
        nextinc = min(nextinc, ni)

    return val, nextinc


def parse_file(datafile) -> (List[range], List[Mapping]):
    seeds = sorted(
        [
            range(start, start + n)
            for start, n in pairs(numbers(datafile.readline().split(":")[1]))
        ],
        key=attrgetter("start"),
    )
    mappings = []

    assert datafile.readline() == "\n"

    while True:
        mapping_tuples = []

        # Read mapping:
        line = datafile.readline()
        assert re.match(r"(\w+)-to-(\w+) map:", line)

        while True:
            line = datafile.readline()
            if ns := numbers(line):
                mapping_tuples.append(ns)
            else:
                break

        mappings.append(Mapping(mapping_tuples))

        if not line:
            break  # eof

    return seeds, mappings


def solve(datafile):
    seed_ranges, mappings = parse_file(datafile)

    result = sys.maxsize
    for seed_range in seed_ranges:
        seed = seed_range.start
        while True:
            val, nextinc = map_all(mappings, seed)
            result = min(val, result)
            if (seed + nextinc) in seed_range:
                seed += nextinc
            else:
                break
    return result


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
    assert seeds == [range(55, 55 + 13), range(79, 79 + 14)]
    m = maps[0]
    assert m.map(79) == (81, 19)
    assert m.map(14) == (14, 36)
    assert m.map(55) == (57, 43)
    assert m.map(13) == (13, 37)


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 46


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 28580589


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
