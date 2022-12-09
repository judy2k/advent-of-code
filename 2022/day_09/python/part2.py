#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys


def parse(datafile):
    return (
        (d, int(n)) for d, n in (line.strip().split(" ") for line in datafile)
    )


def update_h(h, d):
    match d:
        case "L":
            return (h[0] - 1, h[1])
        case "R":
            return (h[0] + 1, h[1])
        case "D":
            return (h[0], h[1] + 1)
        case "U":
            return (h[0], h[1] - 1)


def step(a, b):
    return a + max(-1, min(b - a, 1))


def update_trailing_knot(knot, knot_ahead):
    tx, ty = knot
    hx, hy = knot_ahead

    if abs(hx - tx) > 1 or abs(hy - ty) > 1:
        return (step(tx, hx), step(ty, hy))
    return knot


def solve(datafile):
    instructions = parse(datafile)

    knots = [(0, 0) for n in range(10)]
    tlog = {(0, 0)}
    for d, n in instructions:
        while n > 0:
            knots[0] = update_h(knots[0], d)
            for i in range(1, len(knots)):
                knots[i] = update_trailing_knot(knots[i], knots[i - 1])
            tlog.add(knots[-1])
            n -= 1

    return len(set(tlog))


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


def test_sample():
    from pathlib import Path

    sample_file = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(sample_file) == 1


def test_sample2():
    from pathlib import Path

    sample_file = Path(__file__).parent.parent.joinpath("sample2.txt").open()
    assert solve(sample_file) == 36


def test_input():
    from pathlib import Path

    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 2458


if __name__ == "__main__":
    main()
