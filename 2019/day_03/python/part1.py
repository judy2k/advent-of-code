#!/usr/bin/env python3

import argparse
from collections import namedtuple
import logging
import sys


class Wire:
    def __init__(self):
        self.x = {}
        self.y = {}


def instructions_to_wire(instructions):
    pos = (0, 0)
    wire = Wire()
    for instruction in instructions:
        direction, distance = instruction[0], int(instruction[1:])
        if direction == 'R':
            span = (pos[0], pos[0] + distance)
            pos = (span[1], pos[1])
            wire.y.setdefault(pos[1], []).append(tuple(sorted(span)))
        elif direction == 'L':
            span = (pos[0], pos[0] - distance)
            pos = (span[1], pos[1])
            wire.y.setdefault(pos[1], []).append(tuple(sorted(span)))
        elif direction == 'U':
            span = (pos[1], pos[1] - distance)
            pos = (pos[0], span[1])
            wire.x.setdefault(pos[0], []).append(tuple(sorted(span)))
        elif direction == 'D':
            span = (pos[1], pos[1] + distance)
            pos = (pos[0], span[1])
            wire.x.setdefault(pos[0], []).append(tuple(sorted(span)))
    return wire


def test_instructions_to_wire():
    w = instructions_to_wire('R8,U5,L5,D3'.split(','))
    assert w.x == {
        8: [(-5, 0),],
        3: [(-5, -2)]
    }

    assert w.y == {
        0: [(0, 8),],
        -5: [(3, 8),],
    }


def solve(datafile):
    wire1 = instructions_to_wire(datafile.readline().split(','))
    wire2 = instructions_to_wire(datafile.readline().split(','))

    connections = []
    for x, y_ranges in wire2.x.items():
        for y_range in y_ranges:
            lower, upper = y_range
            for y in range(lower+1, upper):
                if spans := wire1.y.get(y):
                    for span in spans:
                        if span[0] < x <= span[1]:
                            connections.append((x, y))
    for y, x_ranges in wire2.y.items():
        for x_range in x_ranges:
            lower, upper = x_range
            for x in range(lower+1, upper):
                if spans := wire1.x.get(x):
                    for span in spans:
                        if span[0] < y <= span[1]:
                            connections.append((x, y))
    return sorted([abs(x) + abs(y) for x, y in connections if not (x == 0 and y == 0)])[0]


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("datafile", type=argparse.FileType(mode="r"))

    args = ap.parse_args(argv)

    logging.basicConfig(
        format="%(message)s", level=logging.DEBUG if args.verbose else logging.WARNING
    )
    print(solve(args.datafile))


if __name__ == "__main__":
    main()
