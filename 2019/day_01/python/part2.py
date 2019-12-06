#!/usr/bin/env python3

from math import floor


def calculate_fuel(weight):
    new_weight = floor(int(weight) / 3.0) - 2
    if new_weight > 0:
        return new_weight + calculate_fuel(new_weight)
    else:
        return 0

print(sum(calculate_fuel(int(line)) for line in open('input_01.txt', 'r')))
    