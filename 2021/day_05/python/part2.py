#!/usr/bin/env python3

import argparse
import logging
import re
import sys

from collections import Counter
from itertools import chain, takewhile


def solve(datafile):
    lines = [parse_line(line) for line in datafile]
    counts = Counter(chain(*(line.pixels() for line in lines)))
    return len(list(takewhile(lambda kv: kv[1] > 1, counts.most_common())))


def parse_line(line):
    if match := re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line):
        return Line(
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
            int(match.group(4)),
        )


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = min((x1, y1), (x2, y2))
        self.x2, self.y2 = max((x1, y1), (x2, y2))
        self.dx = self.x2 - self.x1
        self.dy = self.y2 - self.y1

    def horv(self):
        return self.dx == 0 or self.dy == 0

    def pixels(self):
        if self.horv():
            if self.dx == 0:
                return [
                    (self.x1, y)
                    for y in range(min(self.y1, self.y2), max(self.y1, self.y2) + 1)
                ]
            else:
                return [(x, self.y1) for x in range(self.x1, self.x2 + 1)]
        else:
            direction = 1 if self.dy > 0 else -1
            return list(
                zip(
                    range(self.x1, self.x2 + 1),
                    range(self.y1, self.y2 + direction, direction),
                )
            )

    def __repr__(self):
        return f"<Line {self.x1},{self.y1} -> {self.x2},{self.y2}>"


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
    assert solve(open("../sample.txt")) == 12


if __name__ == "__main__":
    main()
