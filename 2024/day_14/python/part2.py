#!/usr/bin/env python3

import re
from dataclasses import dataclass
from itertools import count
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


def plot(robots, w, h):
    pos = set((r.x, r.y) for r in robots)
    for row in range(h):
        print("".join("#" if (col, row) in pos else "." for col in range(w)))


def solve(datafile, w, h):
    robots = [
        Robot(*(int(g) for g in match.groups()))
        for match in re.finditer(
            r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", datafile.read()
        )
    ]

    for second in count(start=1):
        for robot in robots:
            robot.update(w, h)
        if (second - 76) % 103 == 0 and (second - 14) % 101 == 0:
            print(f"Second {second}")
            plot(robots, w, h)
            break


def main():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    solve(datafile, 101, 103)


if __name__ == "__main__":
    main()
