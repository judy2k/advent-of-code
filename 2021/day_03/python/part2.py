#!/usr/bin/env python3

import argparse
from collections import Counter
from operator import mul
import logging
import sys


def solve(datafile):
    values = [line.strip() for line in datafile.readlines()]
    oxygen_generator = match_filter(values, oxygen_generator_filter)
    co2_scrubber = match_filter(values, co2_scrubber_filter)

    logging.info("Oxy: %s, CO2: %s", oxygen_generator, co2_scrubber)

    return co2_scrubber * oxygen_generator


def match_filter(values, bit_filter_func):
    for bit_index in range(len(values[0])):
        bit = bit_filter_func(Counter(list(zip(*values))[bit_index]))
        values = list(filter(lambda v: v[bit_index] == bit, values))
        if len(values) == 1:
            return bits_to_int(values[0])
    raise Exception("Never reduced to 1")


def oxygen_generator_filter(counter):
    if counter["1"] == counter["0"]:
        return "1"
    return counter.most_common()[0][0]


def co2_scrubber_filter(counter):
    if counter["1"] == counter["0"]:
        return "0"
    return counter.most_common()[1][0]


def bits_to_int(bits):
    return int("".join(bits), 2)


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
    assert solve(open("../sample.txt")) == 230


if __name__ == "__main__":
    main()
