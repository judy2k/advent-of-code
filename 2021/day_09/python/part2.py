#!/usr/bin/env python3

import argparse
import logging
import sys

from math import prod


def solve(datafile):
    height_map = Grid([[int(c) for c in line.strip()] for line in datafile])
    basins = height_map.find_basins()
    largest_three_basins = sorted([len(basin) for basin in basins])[-3:]
    return prod(largest_three_basins)


class Grid:
    def __init__(self, height_map):
        self.height_map = height_map
        self.row_count = len(self.height_map)
        self.col_count = len(self.height_map[0])

    def get(self, row, col):
        return self.height_map[row][col]

    def surrounding_points(self, row, col):
        points = []
        if row > 0:
            points.append((row - 1, col))
        if col > 0:
            points.append((row, col - 1))
        if col < self.col_count - 1:
            points.append((row, col + 1))
        if row < self.row_count - 1:
            points.append((row + 1, col))
        return points

    def surrounding_heights(self, row, col):
        return [self.get(row, col) for row, col in self.surrounding_points(row, col)]

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

    def flood_fill(self, row, col, filled_points=None):
        if filled_points is None:
            filled_points = set()

        if (row, col) not in filled_points and self.get(row, col) != 9:
            filled_points.add((row, col))
            for row, col in self.surrounding_points(row, col):
                self.flood_fill(row, col, filled_points)

        return filled_points

    def find_basins(self):
        basins = []
        for row, col in self.coords():
            # Check to see if this point is already in a basin:
            for basin in basins:
                if (row, col) in basin:
                    break
            else:
                # If not already in a basin, and not 9,
                # generate a new basin at this point:
                if self.get(row, col) != 9:
                    basins.append(self.flood_fill(row, col))
        return basins


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
    assert solve(open("../sample.txt")) == 1134


if __name__ == "__main__":
    main()
