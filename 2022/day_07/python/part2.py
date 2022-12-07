#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys


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
    root = ds[0]
    free_space = 70_000_000 - root.size()
    required_space = 30_000_000 - free_space

    ds = [d for d in ds if d.size() >= required_space]
    ds.sort(key=lambda d: d.size())

    return ds[0].size()


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


if __name__ == "__main__":
    main()
