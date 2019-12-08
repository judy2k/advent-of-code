#!/usr/bin/env python3

import argparse
from itertools import islice
import logging
from math import floor
import sys


class Processor:
    def __init__(self, program):
        self.program = program
        self.pos = 0
        self.instructions = {1: self.add, 2: self.multiply, 99: self.stop}

    def add(self):
        program = self.program
        pos1, pos2, respos = program[self.pos + 1 : self.pos + 4]
        logging.debug("add(%d, %d, %d)", pos1, pos2, respos)
        program[respos] = program[pos1] + program[pos2]
        self.pos += 4

    def multiply(self):
        program = self.program
        pos1, pos2, respos = program[self.pos + 1 : self.pos + 4]
        logging.debug("mul(%d, %d, %d)", pos1, pos2, respos)
        program[respos] = program[pos1] * program[pos2]
        self.pos += 4

    def stop(self):
        logging.debug("abort()")
        raise StopIteration()

    def __iter__(self):
        return self

    def __next__(self):
        opcode = self.program[self.pos]
        self.instructions[opcode]()


def solve(datafile):
    program = []
    for line in datafile:
        program += [int(s) for s in line.split(",")]

    program[1] = 12
    program[2] = 2

    p = Processor(program)
    for _ in p:
        pass

    return p.program[0]


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
