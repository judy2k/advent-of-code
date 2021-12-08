#!/usr/bin/env python3

import argparse
import logging
import sys

from itertools import takewhile, count, islice, chain


class Grid:
    def __init__(self, numbers):
        self.numbers = [int(n) for n in numbers]
        self.width = 5
        self.height = 5

    def get(self, col, row):
        return self.numbers[row * self.width + col]

    def row(self, index):
        return list(self.numbers[index * self.width : index * self.width + self.width])

    def rows(self):
        for row_index in range(self.height):
            yield self.row(row_index)

    def col(self, index):
        return list(self.numbers[index :: self.width])

    def cols(self):
        for col_index in range(self.width):
            yield self.col(col_index)

    # def positive_diagonal(self):
    #     return [self.get(i, i) for i in range(self.width)]

    # def negative_diagonal(self):
    #     return [self.get(i, self.height - (i + 1)) for i in range(self.width)]

    def lines(self):
        return chain(
            self.rows(),
            self.cols(),
        )


class Board(Grid):
    def has_won(self, called_numbers):
        winning_cells = self.winning_cells(called_numbers)
        # Check rows:
        for line in winning_cells.lines():
            if all(line):
                return True

    def score(self, called_numbers):
        unmarked_numbers = filter(
            None,
            map(
                lambda x: x[0] if not x[1] else None,
                zip(self.numbers, self.winning_cells(called_numbers).numbers),
            ),
        )
        return (
            sum(
                map(
                    lambda x: x[0] if not x[1] else 0,
                    zip(self.numbers, self.winning_cells(called_numbers).numbers),
                )
            )
            * called_numbers[-1]
        )

    def winning_cells(self, called_numbers):
        called_number_set = set(called_numbers)
        return Grid([num in called_number_set for num in self.numbers])


def np(nums):
    print(" ".join("%02d" % i for i in nums))


def dice(seq, n):
    seq = iter(seq)
    return takewhile(len, (tuple(islice(seq, n)) for _ in count()))


def solve(datafile):
    number_seq = [int(w) for w in next(datafile).split(",")]
    boards = list(board_iter(datafile))

    for called_numbers in unbounded_slices(number_seq):
        boards = [board for board in boards if not board.has_won(called_numbers)]
        if len(boards) == 1:
            break

    board = boards[0]
    for called_numbers in unbounded_slices(number_seq):
        if board.has_won(called_numbers):
            return board.score(called_numbers)

    return 0


def read_board(input):
    input.readline()
    numbers = []
    for _ in range(5):
        numbers += [int(w) for w in input.readline().split()]
    return numbers


def board_iter(input):
    while True:
        ns = read_board(input)
        if ns:
            yield Board(ns)
        else:
            return


def unbounded_slices(seq):
    for stop in range(1, len(seq) + 1):
        yield seq[0:stop]


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
    assert solve(open("../sample.txt")) == 4512


def test_dice():
    d = dice(count(), 3)
    assert next(d) == (0, 1, 2)
    assert next(d) == (3, 4, 5)

    d = dice([0, 1, 2, 3, 4], 3)
    assert next(d) == (0, 1, 2)
    assert next(d) == (3, 4)


def test_unbounded_slices():
    us = unbounded_slices([0, 1, 2])

    assert list(next(us)) == [0]
    assert list(next(us)) == [0, 1]
    assert list(next(us)) == [0, 1, 2]


if __name__ == "__main__":
    main()
