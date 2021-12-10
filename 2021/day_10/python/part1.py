#!/usr/bin/env python3

import argparse
import logging
import sys

CLOSING_CHARS = set("})]>")
MATCHING_OPEN = {"]": "[", "}": "{", ")": "(", ">": "<"}
MATCHING_CLOSE = {v: k for k, v in MATCHING_OPEN.items()}
SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def solve(datafile):
    return score([invalid_character(line.strip()) for line in datafile])


def invalid_character(line):
    stack = []
    for i, c in enumerate(line):
        if c in CLOSING_CHARS:
            if (ec := stack.pop()) != MATCHING_OPEN[c]:
                if logging.getLogger().isEnabledFor(logging.INFO):
                    print()
                    print("ERROR ON LINE:", line)
                    print("              ", ("-" * i) + "^")
                    print(
                        f"Expected {MATCHING_CLOSE[ec]}, but found {c} instead, at index {i}"
                    )
                    print("Stack:", "".join(stack))

                return c
        else:
            stack.append(c)


def score(ics):
    return sum(SCORES.get(ic, 0) for ic in ics)


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
    assert solve(open("../sample.txt")) == 26397


if __name__ == "__main__":
    main()
