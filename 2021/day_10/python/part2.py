#!/usr/bin/env python3

import argparse
import logging
import sys

CLOSING_CHARS = set("})]>")
MATCHING_OPEN = {"]": "[", "}": "{", ")": "(", ">": "<"}
MATCHING_CLOSE = {v: k for k, v in MATCHING_OPEN.items()}
SCORES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def solve(datafile):
    completions = filter(None, [complete(line.strip()) for line in datafile])
    scores = sorted(score(completion) for completion in completions)
    return scores[len(scores) // 2]


def complete(line):
    stack = []
    for c in line:
        if c in CLOSING_CHARS:
            if (ec := stack.pop()) != MATCHING_OPEN[c]:
                return None
        else:
            stack.append(c)

    return "".join(MATCHING_CLOSE[open] for open in reversed(stack))


def score(ic):
    score = 0
    for c in ic:
        score *= 5
        score += SCORES[c]

    return score


def test_score():
    assert score("])}>") == 294
    assert score("}}]])})]") == 288957


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
    assert solve(open("../sample.txt")) == 288957


if __name__ == "__main__":
    main()
