#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

import re


class Game:
    def __init__(self, line, id, subsets):
        self.line = line
        self.id = int(id)
        self.subsets = subsets
        self.totals = combine_subsets(subsets)

    def match(self, superset):
        result = all(a >= b for (a, b) in zip(superset, self.totals))

        return result

    @classmethod
    def parse_line(cls, line):
        if match := re.match(r"Game (?P<id>\d+): (?P<groupstr>.*)", line):
            id = match.group("id")
            subsets = [parse_subset(gs) for gs in match.group("groupstr").split("; ")]
            return cls(line, id, subsets)
        else:
            raise Exception(f"Could not parse line: {line}")


def parse_subset(subset):
    return (
        int((m := re.search(r"(\d+) red", subset)) and m.group(1) or 0),
        int((m := re.search(r"(\d+) green", subset)) and m.group(1) or 0),
        int((m := re.search(r"(\d+) blue", subset)) and m.group(1) or 0),
    )


def combine_subsets(subsets):
    return tuple(max(vs) for vs in zip(*subsets))


def solve(datafile, bag):
    tally = 0
    for line in datafile:
        game = Game.parse_line(line)
        if game.match(bag):
            tally += game.id

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
    print(solve(args.datafile, (12, 13, 14)))


from pathlib import Path


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile, (12, 13, 14)) == 8


def test_parse_subset():
    assert parse_subset("3 blue, 4 red") == (4, 0, 3)
    assert parse_subset("1 red, 2 green, 6 blue") == (1, 2, 6)


def test_combine_subsets():
    assert combine_subsets([(4, 0, 3), (1, 2, 6)]) == (4, 2, 6)


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile, (12, 13, 14)) > 198


if __name__ == "__main__":
    main()
