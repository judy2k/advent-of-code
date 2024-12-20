#!/usr/bin/env python3

import argparse
import logging
import sys
from dataclasses import dataclass
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


class Map:
    def __init__(self, mapdata):
        self.grid = Grid(mapdata)
        self.robot_pos = Location(0, 0)
        for (row, col), val in self.grid.cells():
            if val == "@":
                self.robot_pos = Location(row, col)
                break

    def draw(self):
        for row in self.grid.rows:
            print("".join(row))

    def _build_move(self, direction):
        pos = self.robot_pos
        boxes = []
        while True:
            pos = pos.move(direction)
            match self.grid[pos]:
                case ".":
                    return boxes
                case "#":
                    return None
                case "O":
                    boxes.append(pos)
                case None:
                    raise Exception("Somehow ended up out of bounds!")

    def move(self, direction: Direction):
        boxes = self._build_move(direction)
        if boxes is not None:
            for box in reversed(boxes):
                self.grid[box + direction] = "O"
                self.grid[box] = "."
            self.grid[self.robot_pos + direction] = "@"
            self.grid[self.robot_pos] = "."
            self.robot_pos += direction


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
    for move in moves:
        print(f"Move: {REVERSE_DIRECTIONS[move]}")
        map.move(move)
    return sum(
        row * 100 + col for (row, col), val in map.grid.cells() if val == "O"
    )


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


def test_sample1():
    datafile = Path(__file__).parent.parent.joinpath("sample1.txt").open()
    assert solve(datafile) == 2028


def test_sample2():
    datafile = Path(__file__).parent.parent.joinpath("sample2.txt").open()
    assert solve(datafile) == 10092


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 1526018


if __name__ == "__main__":
    main()
