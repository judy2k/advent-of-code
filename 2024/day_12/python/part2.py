#!/usr/bin/env python3

import argparse
import logging
import sys
from itertools import chain, groupby, product
from pathlib import Path

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class Region:
    def __init__(self, grid, starting_pos):
        self.letter = grid[starting_pos[0]][starting_pos[1]]
        self.plots = set()
        self._add_plot(grid, starting_pos)

    def contains(self, plot):
        return plot in self.plots

    def _add_plot(self, grid, pos):
        self.plots.add(pos)
        for direction in DIRECTIONS:
            neighbour = (pos[0] + direction[0], pos[1] + direction[1])
            if (
                0 <= neighbour[0] < len(grid)
                and 0 <= neighbour[1] < len(grid[0])
                and grid[neighbour[0]][neighbour[1]] == self.letter
            ):
                if neighbour not in self.plots:
                    self._add_plot(grid, neighbour)

    def bounding_box(self):
        rows, cols = zip(*self.plots)
        return min(rows), max(rows), min(cols), max(cols)

    def perimeters(self):
        min_row, max_row, min_col, max_col = self.bounding_box()

        perimeters = sum(
            chain(
                # Scan Down (horizontal perimeters)
                (
                    len(
                        [
                            k
                            for k, _ in groupby(
                                [
                                    ((row, col) in self.plots)
                                    - ((row + 1, col) in self.plots)
                                    for col in range(min_col - 1, max_col + 2)
                                ]
                            )
                            if k != 0
                        ]
                    )
                    for row in range(min_row - 1, max_row + 1)
                ),
                # Scan Across (vertical perimeters)
                (
                    len(
                        [
                            k
                            for k, _ in groupby(
                                [
                                    ((row, col) in self.plots)
                                    - (
                                        (
                                            row,
                                            col + 1,
                                        )
                                        in self.plots
                                    )
                                    for row in range(min_row - 1, max_row + 2)
                                ]
                            )
                            if k != 0
                        ]
                    )
                    for col in range(min_col - 1, max_col + 1)
                ),
            )
        )

        return perimeters

    def score(self):
        return len(self.plots) * self.perimeters()


def solve(datafile):
    regions = []

    grid = [list(line.strip()) for line in datafile]

    for row, col in product(range(len(grid)), range(len(grid[0]))):
        for region in regions:
            if region.contains((row, col)):
                break
        else:
            regions.append(Region(grid, (row, col)))

    return sum(region.score() for region in regions)


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


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 1206


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 910066


if __name__ == "__main__":
    main()
