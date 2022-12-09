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


def update_t(t, h):
    tx, ty = t
    hx, hy = h

    if abs(hx - tx) > 1 or abs(hy - ty) > 1:
        return (step(tx, hx), step(ty, hy))
    return t


def solve(datafile):
    h = (0, 0)
    t = (0, 0)
    tlog = {(0, 0)}

    for d, n in parse(datafile):
        while n > 0:
            h = update_h(h, d)
            t = update_t(t, h)
            tlog.add(t)
            n -= 1

    return len(tlog)


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

    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 13


def test_input():
    from pathlib import Path

    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 6271


if __name__ == "__main__":
    main()
