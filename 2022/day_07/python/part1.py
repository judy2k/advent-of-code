#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys
from functools import lru_cache


class Directory:
    def __init__(self):
        self.files = []
        self.dirs = {}

    def size(self) -> int:
        result = sum(f[1] for f in self.files) + sum(
            d.size() for _, d in self.dirs.items()
        )
        return result


def parse_datafile(datafile) -> Directory:
    directories = []
    stack = []

    for line in datafile:
        line = line.strip().split(" ")
        if line[0] == "$":
            command = line[1:]
            if command[0] == "cd":
                if command[1] == "..":
                    stack.pop()
                else:
                    stack.append(Directory())
                    if len(stack) > 1:
                        stack[-2].dirs[command[1]] = stack[-1]
                    directories.append(stack[-1])
        else:
            if line[0] == "dir":
                pass
            else:
                stack[-1].files.append((line[1], int(line[0])))

    return directories


def solve(datafile):
    ds = parse_datafile(datafile)
    result = sum(d.size() for d in ds if d.size() <= 100000)
    return result


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
    assert solve(sample_file) == 95_437


def test_input():
    from pathlib import Path

    input_file = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(input_file) == 1_423_358


if __name__ == "__main__":
    main()
