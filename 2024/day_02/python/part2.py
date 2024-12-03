#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info
from pathlib import Path
import sys
from collections import Counter


def solve(datafile):
    safe = 0

    for line in datafile:
        ns = [int(t) for t in line.strip().split()]
        s = is_safe(ns)
        if s:
            safe += 1

    return safe


def sign(n):
    return -1 if n < 0 else 1 if n > 0 else 0


def is_safe(ns: list[int]) -> bool:
    sign_counter = Counter([sign(d) for d in [b - a for a, b in list(zip(ns, ns[1:]))[:4]]])
    direction = sign_counter.most_common()[0][0]

    return check_levels(ns, direction, True)


def check_levels(ns: list[int], direction: int, can_relax):
    idx = 0
    while idx < len(ns) - 1:
        if not 1 <= (ns[idx + 1] - ns[idx]) * direction <= 3:
            return can_relax and (
                check_levels(
                    ns[max(idx - 1, 0) : idx] + ns[idx + 1 :], direction, False
                )  # Try without idx
                or check_levels(
                    ns[ max(idx, 0) : idx + 1] + ns[idx + 2 :], direction, False
                )  # Try without idx+1
            )
        idx += 1
    return True


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


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 4


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 328


if __name__ == "__main__":
    main()
