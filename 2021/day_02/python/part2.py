#!/usr/bin/env python3

import argparse
import logging
import sys


def solve(datafile):
    horizontal = 0
    depth = 0
    aim = 0
    for direction, distance in (parse_line(line) for line in datafile):
        if direction == "forward":
            horizontal += distance
            depth += aim * distance
        elif direction == "down":
            aim += distance
        elif direction == "up":
            aim -= distance
        else:
            raise Exception(f"Unknown direction: {direction}")
    logging.info(f"Final position: (h: {horizontal}, d: {depth})")
    return horizontal * depth


def parse_line(line):
    direction, distance = line.split(" ", 1)
    return (direction, int(distance))


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
    assert solve(open("../sample.txt")) == 900


if __name__ == "__main__":
    main()
