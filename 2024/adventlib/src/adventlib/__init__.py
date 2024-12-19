"""A library to make working with Advent of Code problems slightly less repetitive."""

from . import grid
from .grid import Direction, Grid, Location  # noqa: F401

__all__ = ["grid"]
