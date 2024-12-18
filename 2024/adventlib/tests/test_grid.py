import io
from collections.abc import Iterable

from adventlib import Grid, Location
from adventlib.grid import Direction


def test_basic():
    grid = Grid.read(
        io.StringIO("""a b c
    d e f""")
    )
    assert grid[0, 0] == "a"
    assert isinstance(grid[0, 0], str)
    assert grid[Location(1, 2)] == "f"
    assert grid.height == 2
    assert grid.width == 3

    assert grid[-1, 0] is None
    assert grid[2, 0] is None
    assert grid[0, -1] is None
    assert grid[0, 3] is None

    assert not grid.in_bounds(0, 3)
    assert grid.in_bounds(0, 2)
    assert grid.in_bounds(Location(0, 2))
    assert not grid.in_bounds(Location(0, 3))

    adj = list(grid.adjacent(Location(0, 0), include_diagonals=False))
    adj.sort()
    assert len(adj) == 2


def test_ints():
    grid: Grid[int] = Grid.read(
        io.StringIO("""1 2 3
    44 55 66"""),
        converter=int,
    )
    assert grid[1, 2] == 66
    assert isinstance(grid[1, 2], int)


def test_Direction_clockwise():
    directions = Direction.all()
    for i, d in enumerate(directions):
        assert d.clockwise() == directions[(i + 1) % 4]


def test_Direction_anticlockwise():
    directions = Direction.all()
    for i, d in enumerate(directions):
        assert d.anticlockwise() == directions[(i - 1) % 4]


def test_Location_iterable():
    loc = Location(1, 2)
    i = iter(loc)
    assert next(i) == 1
    assert next(i) == 2
    assert isinstance(loc, Iterable)


def test_Location_sort():
    a = Location(1, 1)
    b = Location(1, 0)
    c = Location(0, 1)

    assert list(sorted([a, b, c])) == [c, b, a]
