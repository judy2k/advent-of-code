#!/usr/bin/env python3

import argparse
import io
import logging
import sys
from itertools import product
from pathlib import Path

from tqdm import tqdm

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
PERIMETER_OFFSETS = [
    # Each pair is starting (offset, direction).
    # Perimeter always keeps the region to the right-hand side of travel.
    # Offset is (0, 0) starting at the top-left corner of the plot.
    # The order of these offsets is the same as the order of DIRECTIONS,
    # assuming the direction is the direction looking out of the region.
    # (Perpendicular to the perimeter)
    [(0, 0), (0, 1)],
    [(0, 1), (1, 0)],
    [(1, 1), (0, -1)],
    [(1, 0), (-1, 0)],
]


class Region:
    def __init__(self, grid, starting_pos):
        self.letter = grid[starting_pos[0]][starting_pos[1]]
        self.plots = set()
        self.perimeters = {}
        self._add_plot(grid, starting_pos)

    def contains(self, plot):
        return plot in self.plots

    def _add_plot(self, grid, pos):
        self.plots.add(pos)
        for direction, (p_offset, p_direction) in zip(
            DIRECTIONS, PERIMETER_OFFSETS
        ):
            neighbour = (pos[0] + direction[0], pos[1] + direction[1])
            if (
                0 <= neighbour[0] < len(grid)
                and 0 <= neighbour[1] < len(grid[0])
                and grid[neighbour[0]][neighbour[1]] == self.letter
            ):
                if neighbour not in self.plots:
                    self._add_plot(grid, neighbour)
            else:
                self.perimeters[
                    (pos[0] + p_offset[0], pos[1] + p_offset[1])
                ] = p_direction

    def p_score(self):
        print(f"SCORE: {self.letter}")
        loc, direction = next(iter(self.perimeters.items()))
        # Find a corner:
        while True:
            loc2 = (loc[0] + direction[0], loc[1] + direction[1])
            direction2 = self.perimeters.get(loc2)
            if direction2 != direction:
                break
            loc, direction = loc2, direction2

        start_loc = loc
        length = 0
        for _ in range(len(self.perimeters)):
            loc2 = (loc[0] + direction[0], loc[1] + direction[1])
            direction2 = self.perimeters.get(loc2)
            print(f"{loc} -> {direction}, {loc2} -> {direction2}")
            if direction2 != direction:
                print("   Increment direction")
                length += 1
            if loc2 == start_loc:
                break
            loc, direction = loc2, direction2
        else:
            raise Exception("Looping perimeters!")
        return length

    def score(self):
        p_score = self.p_score()
        print(f"{self.letter}: {len(self.plots)} x {p_score}")
        return len(self.plots) * p_score


def solve(datafile):
    regions = []

    grid = [list(line.strip()) for line in datafile]

    for row, col in product(range(len(grid)), range(len(grid[0]))):
        for region in regions:
            if region.contains((row, col)):
                break
        else:
            regions.append(Region(grid, (row, col)))

    return sum(region.score() for region in tqdm(regions))


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


def test_enclosed():
    datafile = io.StringIO("""AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA""")
    assert solve(datafile) == 368


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 1206


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 1533024


if __name__ == "__main__":
    main()
