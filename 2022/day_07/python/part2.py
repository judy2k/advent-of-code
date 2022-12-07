#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

import re
from collections import namedtuple

Directory = namedtuple("Directory", ["files", "dirs"])


def size(files, dirs) -> int:
    return sum(f[1] for f in files) + sum(size(*d) for _, d in dirs.items())


def parse_datafile(datafile) -> Directory:
    directories = []
    stack = []

    for line in datafile:
        tokens = re.match(r"((?:\$ )?\w+)(?: (.*)?)?", line.strip()).groups()
        if tokens[0] == "$ cd":
            if tokens[1] == "..":
                stack.pop()
            else:
                stack.append(Directory([], {}))
                if len(stack) > 1:
                    stack[-2].dirs[tokens[1]] = stack[-1]
                directories.append(stack[-1])
        elif tokens[0] in {"dir", "$ ls"}:
            pass
        else:
            stack[-1].files.append((tokens[1], int(tokens[0])))

    return directories


def solve(datafile):
    ds = parse_datafile(datafile)

    return size(
        *sorted(
            [
                d
                for d in ds
                if size(*d) >= 30_000_000 - (70_000_000 - size(*ds[0]))
            ],
            key=lambda d: size(*d),
        )[0]
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
    print(solve(args.datafile))


def test_sample():
    from pathlib import Path

    sample_file = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(sample_file) == 24933642


def test_input():
    from pathlib import Path

    input_file = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(input_file) == 545729


if __name__ == "__main__":
    main()
