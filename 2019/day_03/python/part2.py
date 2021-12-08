#!/usr/bin/env python3

import argparse
from collections import namedtuple
import logging
import sys


class Wire:
    def __init__(self):
        self.points = []


def instructions_to_wire(instructions):
    pos = (0, 0)
    wire = Wire()
    for instruction in instructions:
        direction, distance = instruction[0], int(instruction[1:])
        if direction == 'R':
            span = [pos[0], pos[0] + distance]
            pos = (span[1], pos[1])
            wire.points.extend((x, pos[1]) for x in range(span[0], span[1]+1))
        elif direction == 'L':
            span = (pos[0], pos[0] - distance)
            pos = (span[1], pos[1])
            wire.points.extend((x, pos[1]) for x in range(span[0], span[1]-1))
        elif direction == 'U':
            span = (pos[1], pos[1] - distance)
            pos = (pos[0], span[1])
            wire.points.extend((pos[0], y) for y in range(span[0], span[1]-1))
        elif direction == 'D':
            span = (pos[1], pos[1] + distance)
            pos = (pos[0], span[1])
            wire.points.extend((pos[0], y) for y in range(span[0], span[1]+1))
    return wire


def solve(datafile):
    wire1 = instructions_to_wire(datafile.readline().split(','))
    wire2 = instructions_to_wire(datafile.readline().split(','))

    intersections = set(wire1.points) & set(wire2.points)
    print(intersections)
    for intersection in intersections:
        print(intersection)
        wire1.points.index(intersection) + wire2.points.index(intersection)
    return sorted(wire1.points.index(intersection) + wire2.points.index(intersection) for intersection in intersections)


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
