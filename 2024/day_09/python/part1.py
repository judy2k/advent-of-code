#!/usr/bin/env python3

import argparse
import logging
import sys
from collections.abc import Iterator
from itertools import chain, islice, tee, zip_longest
from pathlib import Path


def pairs(iters) -> Iterator[tuple[int, int | None]]:
    window_size = 2
    return zip_longest(
        *(
            islice(it, i, None, window_size)
            for i, it in enumerate(tee(iters, window_size))
        )
    )  # type: ignore


def solve(datafile):
    input_ints = (int(t) for t in datafile.read().strip())

    file_id = 0
    filesystem = []
    for block_count, empty_space in pairs(input_ints):
        # Append (file_id, block_count) in an array for appending:
        filesystem.append([(file_id, block_count)])
        if empty_space is not None:
            # Append an int containing empty space:
            filesystem.append(empty_space)

        file_id += 1

    current_empty = 1
    defrag = len(filesystem) - 1

    while defrag > current_empty:
        file_id, blocks = filesystem[defrag][0]
        space = filesystem[current_empty]

        blocks_to_move = min(space, blocks)
        filesystem[defrag][0] = (file_id, blocks - blocks_to_move)
        filesystem[current_empty - 1].append((file_id, blocks_to_move))  # dest
        filesystem[current_empty] -= blocks_to_move  # update empty

        if filesystem[defrag][0][1] == 0:
            defrag -= 2

        while filesystem[current_empty] == 0:
            current_empty += 2

    file_blocks = (
        pair for pair in chain.from_iterable(islice(filesystem, None, None, 2))
    )

    tally = 0
    pos = 0
    for item in file_blocks:
        if isinstance(item, tuple):
            file_id, count = item
            tally += int(file_id * ((pos * count) + (count * (count - 1) / 2)))
            pos += count
        else:
            pos += item

    return tally


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


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 1928


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 6446899523367


if __name__ == "__main__":
    main()
