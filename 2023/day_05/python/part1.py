#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import sys

from itertools import dropwhile
import re


def numbers(s):
    return tuple([int(i) for i in re.split(r'\s+', s.strip())])


def map_all(maps, val, map_from="seed"):
    while True:
        map_from, val = maps[map_from].map(val)
        if map_from == "location":
            return val


class Map:
    def __init__(self, map_to, mapping_tuples):
        self.map_to = map_to
        self.mapping_tuples = sorted(mapping_tuples, reverse=True)
    
    def map(self, from_val) -> (str, int):
        mt = iter(self.mapping_tuples)
        item = next(dropwhile(lambda t: t[0] > from_val, mt), None)
        if item:
            s, d, n = item
            if s <= from_val < s + n:
                return self.map_to, from_val - s + d
        return self.map_to, from_val


def parse_file(datafile):
    seeds = numbers(datafile.readline().split(':')[1])
    maps = {}
    
    assert datafile.readline() == '\n'
    
    map_from, map_to = None, None
    mapping_tuples = []
    while True:
        # Read mapping:
        line = datafile.readline()
        if match := re.match(r'(\w+)-to-(\w+) map:', line):
            map_from, map_to = match.groups()
        elif line in {'', '\n'}:
            maps[map_from] = Map(map_to, mapping_tuples)

            map_from, map_to = None, None
            mapping_tuples = []
            if not line:
                break # eof
        else:
            d, s, n = numbers(line)
            mapping_tuples.append((s, d, n))

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
    m = maps["seed"]
    assert m.mapping_tuples[0] == (98, 50, 2)
    assert m.map(79) == ("soil", 81)
    assert m.map(14) == ("soil", 14)
    assert m.map(55) == ("soil", 57)
    assert m.map(13) == ("soil", 13)

def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 35


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 240320250


if __name__ == "__main__":
    main()
