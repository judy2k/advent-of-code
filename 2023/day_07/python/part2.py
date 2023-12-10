#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import sys

from collections import Counter
from functools import total_ordering


card_ranks = {k: v for v, k in enumerate(list(reversed("AKQT98765432J")))}


@total_ordering
class Hand:
    def __init__(self, hand_s):
        self.hand_s = hand_s

        counts = Counter(hand_s)
        j = counts.pop("J", 0)
        if j == 5:
            k = "A"
        else:
            k, _ = counts.most_common()[0]
        counts[k] += j
        self.c = tuple(count for _, count in counts.most_common())

    def __eq__(self, other):
        return self.hand_s == other.hand_s

    def __lt__(self, other):
        if self.c < other.c:
            return True
        elif (
            self.c == other.c
        ):  # self.c and other.c are the same, go to the second method:
            for sc, oc in zip(self.hand_s, other.hand_s):
                if sc != oc:
                    return card_ranks[sc] < card_ranks[oc]
        return False

    def __repr__(self) -> str:
        return f"{self.hand_s} ({self.c})"


def parse_file(datafile) -> (Counter, int):
    for line in datafile:
        hand_s, bid_s = line.strip().split(" ")
        yield Hand(hand_s), int(bid_s)


def solve(datafile):
    hand_bids = sorted(parse_file(datafile))
    return sum(rank * bid for rank, (_, bid) in enumerate(hand_bids, start=1))


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


def test_card_comparison():
    for other in ["T55J5", "KK677", "KTJJT", "QQQJA"]:
        assert Hand("32T3K") < Hand(other)
    for other in ["T55J5", "KTJJT", "QQQJA"]:
        assert Hand("KK677") < Hand(other)

    for other in ["KTJJT", "QQQJA"]:
        assert Hand("T55J5") < Hand(other)

    for other in ["T55J5", "KK677", "QQQJA"]:
        assert Hand("KTJJT") > Hand(other)

    assert Hand("32T3K") == Hand("32T3K")
    assert Hand("KTJJT") > Hand("KK677")


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()

    assert solve(datafile) == 5905


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 251735672


if __name__ == "__main__":
    main()
