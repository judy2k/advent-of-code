#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

import io


class Machine:
    def __init__(self, instructions):
        self.instructions = instructions
        self.tokens = None
        self.x = 1
        self.cycle = 1
        self.iset = {f.__name__: f for f in [self.addx, self.noop]}

    def addx(self, val):
        yield
        yield
        self.x += val

    def noop(self):
        yield

    def interpret(self, line):
        cmd, *args = line.strip().split(" ")
        args = [int(a) for a in args]
        self.tokens = [cmd, *args]

        f = self.iset[cmd](*args)
        try:
            while True:
                next(f)
                info(f"{self.cycle:01d}: x={self.x} ({line.strip()})")
                yield
                self.cycle += 1
        except StopIteration:
            pass

    def run(self):
        for line in self.instructions:
            yield from self.interpret(line)

    def xs(self):
        for _ in self.run():
            yield self.cycle, self.x

    def render(self):
        pixels = [
            "\u2588" if ((cycle - 1) % 40 in range(x - 1, x + 2)) else " "
            for cycle, x in self.xs()
        ]

        result = io.StringIO()

        for row in range(6):
            result.write("".join(pixels[row * 40 : row * 40 + 40]))
            result.write("\n")

        return result.getvalue()


def solve(datafile):
    m = Machine(datafile.readlines())
    return m.render()


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


import pytest
from pathlib import Path


def test_sample():
    from pathlib import Path

    datafile = Path(__file__).parent.parent.joinpath("sample1.txt").open()
    m = Machine(datafile.readlines())
    assert list(m.xs()) == [(1, 1), (2, 1), (3, 1), (4, 4), (5, 4)]
    assert m.x == -1


def test_sample2():
    datafile = Path(__file__).parent.parent.joinpath("sample2.txt").open()
    assert (
        solve(datafile)
        == """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""
    )


if __name__ == "__main__":
    main()
