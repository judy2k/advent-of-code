#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
from pathlib import Path
import sys

from collections import Counter
from functools import total_ordering


card_ranks = {k: v for v, k in enumerate(list(reversed("AKQJT98765432")))}


@total_ordering
class Hand:
    def __init__(self, hand_s):
        self.hand_s = hand_s
        self.c = tuple(count for _, count in Counter(hand_s).most_common())

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
    winnings = 0
    for rank, hand_bid in enumerate(hand_bids, start=1):
        _, bid = hand_bid
        winnings += rank * bid

    return winnings


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
    assert Hand("32T3K") == Hand("32T3K")
    assert Hand("KTJJT") < Hand("KK677")
    for other in ["T55J5", "KK677", "KTJJT", "QQQJA"]:
        assert Hand("32T3K") < Hand(other)


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()

    assert solve(datafile) == 6440


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 250370104


if __name__ == "__main__":
    main()
