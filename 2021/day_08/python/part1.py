#!/usr/bin/env python3

import argparse
import logging
import sys

from collections import Counter
from itertools import chain

masks = {  # Segment count
    0: "abc_efg",  #     6
    1: "__c__f_",  # 2
    2: "a_cde_g",  #    5
    3: "a_cd_fg",  #    5
    4: "_bcd_f_",  #   4
    5: "ab_d_fg",  #    5
    6: "ab_defg",  #     6
    7: "a_c__f_",  #  3
    8: "abcdefg",  #      7
    9: "abcd_fg",  #     6
}  #    8687497    # <- Segment frequency
masks = {k: frozenset(v.replace("_", "")) for k, v in masks.items()}
digit_lookup = {v: k for k, v in masks.items()}


def solve(datafile):
    digit_counter = Counter()
    for line in datafile:
        signal_patterns, digits = parse_line(line)
        key = key_for_patterns(signal_patterns)
        digit_counter.update(map_digit(digit, key) for digit in digits)
    return digit_counter[1] + digit_counter[4] + digit_counter[7] + digit_counter[8]


def map_digit(digit, key):
    translated = frozenset(key[segment] for segment in digit)
    return digit_lookup[translated]


def key_for_patterns(signal_patterns):
    key = {}
    patterns_by_length = {len(pattern): pattern for pattern in signal_patterns}

    # This is a reverse key, maps plaintext -> cyphertext
    key["a"] = next(iter(patterns_by_length[3] - patterns_by_length[2]))

    counts = {v: k for k, v in Counter(chain(*signal_patterns)).items()}
    key["e"] = counts[4]
    key["b"] = counts[6]
    key["f"] = counts[9]
    key["c"] = next(iter(patterns_by_length[3] - {key["a"], key["f"]}))
    key["d"] = next(iter(patterns_by_length[4] - {key["b"], key["c"], key["f"]}))
    key["g"] = next(iter(patterns_by_length[7] - set(key.values())))

    return {v: k for k, v in key.items()}


def parse_line(line):
    signal_pattern_part, output_part = line.split("|", 1)
    signal_patterns = [set(seq) for seq in signal_pattern_part.split()]
    output = output_part.split()
    return signal_patterns, output


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
    assert solve(open("../sample.txt")) == 26


if __name__ == "__main__":
    main()
