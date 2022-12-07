#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys
from typing import Iterable


class Directory:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.dirs = {}

    def subdirectories(self) -> Iterable["Directory"]:
        result = list(self.dirs.values())
        for d in self.dirs.values():
            result.extend(d.subdirectories())
        return result

    def size(self) -> int:
        result = sum(f[1] for f in self.files) + sum(
            d.size() for _, d in self.dirs.items()
        )
        return result

    def __repr__(self):
        return f"Directory({self.name})"


def parse_datafile(datafile) -> Directory:
    root = Directory("/")
    stack = [root]

    for line in datafile:
        line = line.strip().split(" ")
        if line[0] == "$":
            command = line[1:]
            if command[0] == "ls":
                continue
            else:
                if command[0] == "cd":
                    if command[1] == "..":
                        stack.pop()
                    elif command[1] == "/":
                        continue
                    else:
                        stack.append(stack[-1].dirs[command[1]])
        else:
            if line[0] == "dir":
                stack[-1].dirs[line[1]] = Directory(line[1])
            else:
                stack[-1].files.append((line[1], int(line[0])))

    return stack[0]


def solve(datafile):
    root = parse_datafile(datafile)
    free_space = 70_000_000 - root.size()
    required_space = 30_000_000 - free_space

    ds = [d for d in root.subdirectories() if d.size() >= required_space]
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


def test_sample_parse():
    from pathlib import Path

    sample_file = Path(__file__).parent.parent.joinpath("sample.txt").open()
    root = parse_datafile(sample_file)
    a = root.dirs["a"]
    e = a.dirs["e"]
    d = root.dirs["d"]

    assert d.dirs == {}
    assert e.files == [("i", 584)]
    assert e.size() == 584
    assert a.size() == 94853
    assert d.size() == 24933642

    assert root.size() == 48381165


def test_subdirectories():
    a = Directory("a")
    b = Directory("b")
    c = Directory("c")
    d = Directory("d")
    a.dirs["b"] = b
    a.dirs["d"] = d
    b.dirs["c"] = c

    print(a.subdirectories())
    assert a.subdirectories() == [b, d, c]


if __name__ == "__main__":
    main()
