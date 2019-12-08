#!/usr/bin/env python3

from math import floor


print(sum(floor(int(line) / 3.0) - 2 for line in open("input_01.txt", "r")))
