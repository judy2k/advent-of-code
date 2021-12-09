#!/usr/bin/env python3

import argparse
import logging
import sys


def solve(datafile):
    height_map = Grid([[int(c) for c in line.strip()] for line in datafile])
    return sum(h + 1 for h in height_map.low_points())


class Grid:
    def __init__(self, height_map):
        self.height_map = height_map
        self.row_count = len(self.height_map)
        self.col_count = len(self.height_map[0])

    def get(self, row, col):
        return self.height_map[row][col]

    def surrounding_heights(self, row, col):
        pixels = []
        if row > 0:
            pixels.append(self.get(row - 1, col))
        if col > 0:
            pixels.append(self.get(row, col - 1))
        if col < self.col_count - 1:
            pixels.append(self.get(row, col + 1))
        if row < self.row_count - 1:
            pixels.append(self.get(row + 1, col))
        return pixels

    def coords(self):
        for row in range(self.row_count):
            for col in range(self.col_count):
                yield (row, col)

    def low_points(self):
        low_points = []
        for row, col in self.coords():
            if self.get(row, col) < min(self.surrounding_heights(row, col)):
                low_points.append(self.get(row, col))
        return low_points


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
    assert solve(open("../sample.txt")) == 15


if __name__ == "__main__":
    main()
