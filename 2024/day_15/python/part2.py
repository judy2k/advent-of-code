#!/usr/bin/env python3

import argparse
import logging
import sys
from dataclasses import dataclass
from itertools import chain
from pathlib import Path

from adventlib import Direction, Grid, Location


@dataclass
class Box:
    row: int
    col: int


@dataclass
class Robot:
    row: int
    col: int


def double_wide(c):
    match c:
        case "O":
            yield "["
            yield "]"
        case "@":
            yield "@"
            yield "."
        case o:
            yield o
            yield o


class Map:
    def __init__(self, mapdata):
        self.grid = Grid(
            [
                list(chain.from_iterable(double_wide(c) for c in row))
                for row in mapdata
            ]
        )
        self.robot_pos = Location(0, 0)
        for (row, col), val in self.grid.cells():
            if val == "@":
                self.robot_pos = Location(row, col)
                break

    def draw(self):
        for row in self.grid.rows:
            print("".join(row))

    def check_row_for_blockages(self, row: int, previous_row: set):
        result = set()
        for loc in previous_row:
            match self.grid[row, loc.col]:
                case "#":
                    return None
                case "[":
                    result.add(Location(row, loc.col))
                    result.add(Location(row, loc.col).right())
                case "]":
                    result.add(Location(row, loc.col))
                    result.add(Location(row, loc.col).left())
        return result

    def check_col_for_blockages(self, col: int, previous_col: set):
        result = set()
        for loc in previous_col:
            match self.grid[(loc.row, col)]:
                case "#":
                    return None
                case "[" | "]":
                    result.add(Location(loc.row, col))
        return result

    def move(self, direction):
        line_blocks = [
            set([self.robot_pos]),
        ]

        if direction == Direction(row=1, col=0):
            for row in range(self.robot_pos.row + 1, self.grid.height):
                blocks = self.check_row_for_blockages(row, line_blocks[-1])
                if blocks is None:
                    return None
                line_blocks.append(blocks)
        elif direction == Direction(row=-1, col=0):
            for row in reversed(range(self.robot_pos.row)):
                blocks = self.check_row_for_blockages(row, line_blocks[-1])
                if blocks is None:
                    return None
                line_blocks.append(blocks)
        elif direction == Direction(row=0, col=1):
            for col in range(self.robot_pos.col + 1, self.grid.width):
                blocks = self.check_col_for_blockages(col, line_blocks[-1])
                if blocks is None:
                    return None
                line_blocks.append(blocks)
        elif direction == Direction(row=0, col=-1):
            for col in reversed(range(self.robot_pos.col)):
                blocks = self.check_col_for_blockages(col, line_blocks[-1])
                if blocks is None:
                    return None
                line_blocks.append(blocks)

        moves = sorted(list(chain.from_iterable(line_blocks)))
        if direction.col == 1 or direction.row == 1:
            moves = reversed(moves)
        for cell in moves:
            if self.grid[cell] == "@":
                self.robot_pos = cell + direction
            self.grid[cell + direction] = self.grid[cell]
            self.grid[cell] = "."


DIRECTIONS = {
    ">": Direction(0, 1),
    "<": Direction(0, -1),
    "^": Direction(-1, 0),
    "v": Direction(1, 0),
}
REVERSE_DIRECTIONS = {v: k for k, v in DIRECTIONS.items()}


def solve(datafile):
    lines = []
    while (line := datafile.readline().strip()) != "":
        lines.append(list(line))

    moves = [DIRECTIONS[c] for c in datafile.read().strip() if c in DIRECTIONS]
    map = Map(lines)
    # map.draw()

    for move in moves:
        # print(f"Move: {REVERSE_DIRECTIONS[move]}")
        # input()
        map.move(move)
        # map.draw()

    return sum(
        row * 100 + col for (row, col), val in map.grid.cells() if val == "["
    )


def main(argv=sys.argv[1:]):
    try:
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--verbose", action="store_true")
        ap.add_argument("datafile", type=argparse.FileType(mode="r"))

        args = ap.parse_args(argv)

        logging.basicConfig(
            format="%(message)s",
            level=logging.DEBUG if args.verbose else logging.WARNING,
        )
        print(solve(args.datafile))
    except KeyboardInterrupt:
        pass


# Tests ------------------------------------------------------------------------


# def test_sample3():
#     datafile = Path(__file__).parent.parent.joinpath("sample3.txt").open()
#     assert solve(datafile) == 2028


def test_sample2():
    datafile = Path(__file__).parent.parent.joinpath("sample2.txt").open()
    assert solve(datafile) == 9021


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 1550677


if __name__ == "__main__":
    main()
