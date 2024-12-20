#!/usr/bin/env python3

import re
from collections import Counter
from dataclasses import dataclass
from functools import reduce
from operator import mul
from pathlib import Path


@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int

    def update(self, w, h):
        self.x = (self.x + self.vx) % w
        self.y = (self.y + self.vy) % h

    def quadrant(self, w, h):
        cx = w // 2
        cy = h // 2
        if self.x == cx or self.y == cy:
            return None
        return (self.x < cx, self.y < cy)


def solve(datafile, w, h):
    robots = [
        Robot(*(int(g) for g in match.groups()))
        for match in re.finditer(
            r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", datafile.read()
        )
    ]

    for second in range(100):
        for robot in robots:
            robot.update(w, h)

    c = Counter(
        quadrant
        for quadrant in [robot.quadrant(w, h) for robot in robots]
        if quadrant is not None
    )

    return reduce(mul, c.values(), 1)


# Tests ------------------------------------------------------------------------


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile, 11, 7) == 12


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile, 101, 103) == -1
