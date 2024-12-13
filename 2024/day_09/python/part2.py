#!/usr/bin/env python3

import argparse
import logging
import sys
from collections.abc import Iterator
from itertools import islice, tee, zip_longest
from pathlib import Path
from typing import Any

from tqdm import tqdm


def pairs(iters) -> Iterator[tuple[Any, Any | None]]:
    window_size = 2
    return zip_longest(
        *(
            islice(it, i, None, window_size)
            for i, it in enumerate(tee(iters, window_size))
        )
    )  # type: ignore


def defrag(filesystem):
    # Pointer to the file being considered:
    defrag = len(filesystem) - 1

    for defrag in tqdm(range(len(filesystem) - 1, 0, -2)):
        file_id, blocks = filesystem[defrag][0]

        for space_idx in range(1, defrag, 2):
            if filesystem[space_idx] >= blocks:
                # Move file:
                filesystem[defrag][0] = (file_id, 0)  # src
                filesystem[defrag - 1] += blocks  # src space
                filesystem[space_idx - 1].append((file_id, blocks))  # dest
                filesystem[space_idx] -= blocks  # update space
                break


def checksum(filesystem):
    tally = 0
    pos = 0
    for files, space_count in pairs(filesystem):
        for file_id, count in files:
            tally += int(file_id * ((pos * count) + (count * (count - 1) / 2)))
            pos += count
        if space_count is not None:
            pos += space_count

    return tally


def read_input(datafile):
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

    return filesystem


def solve(datafile):
    filesystem = read_input(datafile)
    defrag(filesystem)
    return checksum(filesystem)


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


def test_checksum():
    assert (
        checksum(
            [
                [
                    (0, 2),
                    (9, 2),
                    (2, 1),
                    (1, 3),
                    (7, 3),
                ],
                1,
                [
                    (4, 2),
                ],
                1,
                [
                    (3, 3),
                ],
                4,
                [
                    (5, 4),
                ],
                1,
                [
                    (6, 4),
                ],
                5,
                [
                    (8, 4),
                ],
                2,
            ]
        )
        == 2858
    )


def test_sample():
    datafile = Path(__file__).parent.parent.joinpath("sample.txt").open()
    assert solve(datafile) == 2858


def test_input():
    datafile = Path(__file__).parent.parent.joinpath("input.txt").open()
    assert solve(datafile) == 6478232739671


if __name__ == "__main__":
    main()
