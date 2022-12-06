#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

from itertools import islice, tee


def solve(datafile, n_len):
    return next(
        i + n_len
        for i, n in enumerate(
            zip(
                *(
                    islice(c, i, None)
                    for i, c in enumerate(tee(datafile.read(), n_len))
                )
            )
        )
        if len(set(n)) == n_len
    )


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("datafile", type=argparse.FileType(mode="r"))

    args = ap.parse_args(argv)

    logging.basicConfig(
        format="%(message)s",
        level=logging.DEBUG if args.verbose else logging.WARNING,
    )
    print(solve(args.datafile, 14))


def test_sample():
    assert solve(open("../sample.txt"), 14) == 19


if __name__ == "__main__":
    main()
