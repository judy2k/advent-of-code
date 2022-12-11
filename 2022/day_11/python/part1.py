#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warn
import sys

import attrs
import functools
import operator
import re
from typing import List, Any, Callable

MONKEY_RE = re.compile(
    r"""Monkey \d+:
  Starting items: (?P<starting_items>.*)
  Operation: new = (?P<op>.*)
  Test: divisible by (?P<divisible_by>.*)
    If true: throw to monkey (?P<true_dest>\d+)
    If false: throw to monkey (?P<false_dest>\d+)""",
    re.MULTILINE,
)

OPERATORS = {
    "*": operator.__mul__,
    "+": operator.__add__,
    "-": operator.__sub__,
    "/": operator.__floordiv__,
}


def memo(v):
    def value_wrapper(old):
        return v

    value_wrapper.__repr__ = lambda: f"memo({v})"

    return value_wrapper


def old(old):
    return old


def wrap_operands(vs):
    return [old if v == "old" else memo(int(v)) for v in vs]


@functools.total_ordering
@attrs.define
class Monkey:
    items: List[int]
    operator: Callable
    operands: List[Any]
    divisible_by: int
    true_dest: int
    false_dest: int
    inspected_count: int = 0

    @classmethod
    def from_match(cls, match):
        starting_items = [
            int(s) for s in match.group("starting_items").split(", ")
        ]
        operation = match.group("op").split(" ")
        operands = wrap_operands([operation[0], operation[2]])

        operator = OPERATORS[operation[1]]

        return cls(
            items=starting_items,
            divisible_by=int(match.group("divisible_by")),
            operands=operands,
            operator=operator,
            true_dest=int(match.group("true_dest")),
            false_dest=int(match.group("false_dest")),
        )

    def step(self, monkeys):
        for item in self.items:
            new_value = self.operator(*[op(item) for op in self.operands]) // 3
            if new_value % self.divisible_by == 0:
                monkeys[self.true_dest].items.append(new_value)
            else:
                monkeys[self.false_dest].items.append(new_value)
            self.inspected_count += 1

        self.items = []

    def __lt__(self, other: "Monkey"):
        return self.inspected_count < other.inspected_count


def parse_monkeys(datafile) -> List[Monkey]:
    return [
        Monkey.from_match(match)
        for match in MONKEY_RE.finditer(datafile.read())
    ]


def solve(datafile):
    ms = parse_monkeys(datafile)
    for _round in range(20):
        for m in ms:
            m.step(ms)
    ms.sort()
    return ms[-2].inspected_count * ms[-1].inspected_count


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


from pathlib import Path
import pytest


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 10605


@pytest.mark.parametrize(
    ["p", "expected"], [("sample.txt", 4), ("input.txt", 8)]
)
def test_parse_monkeys(p, expected):
    datafile = Path(__file__).parent.parent.joinpath(p).open()
    assert len(parse_monkeys(datafile)) == expected


def test_input():
    from pathlib import Path

    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 55458


if __name__ == "__main__":
    main()
