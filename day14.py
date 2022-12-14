from __future__ import annotations

import copy
import dataclasses
import enum
import itertools
from typing import Generic
from typing import TypeVar

import utils


@dataclasses.dataclass(eq=True, frozen=True, slots=True)
class Coord:
    x: int
    y: int

    def __add__(self, other: Coord):
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Coord):
        return Coord(self.x - other.x, self.y - other.y)

    def min(self, other: Coord):
        return Coord(min(self.x, other.x), min(self.y, other.y))

    def max(self, other: Coord):
        return Coord(max(self.x, other.x), max(self.y, other.y))

    def normalize1(self):
        return Coord(self.x // abs(self.x) if self.x != 0 else 0, self.y // abs(self.y) if self.y != 0 else 0)


class Item:
    def default(self):
        raise NotImplementedError


T = TypeVar('T', bound=Item)


def digits(n: int) -> list[int]:
    res: list[int] = []
    while n:
        res.append(n % 10)
        n //= 10
    return list(reversed(res))


class SparseMap(Generic[T]):
    def __init__(self):
        self.lines: list[list[T]] = []
        self.origin: Coord | None = None
        self.size = Coord(0, 0)

    def __contains__(self, item: Coord):
        a = Coord(0, 0)
        b = (item - self.origin)
        c = self.size - Coord(1, 1)
        return a.x <= b.x <= c.x and a.y <= b.y <= c.y

    def __setitem__(self, key: Coord, value: T):
        if self.origin is None:
            self.origin = key
            self.size = Coord(1, 1)
            self.lines = [[value]]
            return

        if key in self:
            coord = key - self.origin
            self.lines[coord.y][coord.x] = value
            return

        previous = copy.deepcopy(self)
        self.origin = previous.origin.min(key)
        max_plus1 = (previous.origin + previous.size - Coord(1, 1)).max(key)
        self.size = max_plus1 - self.origin + Coord(1, 1)
        self.lines = [[value.default() for _ in range(self.size.x)] for _ in range(self.size.y)]

        for y in range(self.size.y):
            for x in range(self.size.x):
                coord = Coord(x, y)
                abs_coord = self.origin + coord
                if abs_coord not in previous:
                    continue
                self.lines[coord.y][coord.x] = previous[abs_coord]

        coord = key - self.origin
        self.lines[coord.y][coord.x] = value

    def __getitem__(self, item: Coord):
        if item not in self:
            raise KeyError
        coord = item - self.origin
        return self.lines[coord.y][coord.x]

    def pprint(self):
        labels_raw = [self.origin.x, self.origin.x + self.size.x - 1]
        checks = [lambda t: t == 0, lambda t: t == self.size.x - 1]
        if self.origin.x <= 500 <= self.origin.x + self.size.x - 1:
            labels_raw.insert(1, 500)
            checks.insert(1, lambda t: self.origin.x + t == 500)
        labels = [digits(n) for n in labels_raw]
        max_len = max(map(len, labels))
        for y in range(max_len):
            print('   ', end='')
            for x in range(self.size.x):
                for i, (label, check) in enumerate(zip(labels, checks)):
                    if check(x):
                        print(labels[i][y] if y < len(labels[0]) else ' ', end='')
                        break
                else:
                    print(' ', end='')
            print()

        for y in range(self.size.y):
            label = self.origin.y + y
            print(f"{label:2d} ", end='')
            for x in range(self.size.x):
                print(self.lines[y][x], end='')
            print()
        print()


class MapItem(Item, enum.StrEnum):
    background = '.'
    wall = '#'
    sand = 'o'
    source = '+'

    def default(self):
        return self.background


def solution(level: int):
    m = SparseMap[MapItem]()
    source = Coord(500, 5)
    m[source] = MapItem.source

    for line in utils.input_reader():
        wall_spline = [Coord(*map(int, coords.split(','))) for coords in line.split(' -> ')]

        for wall_from, wall_to in itertools.pairwise(wall_spline):
            vel = (wall_to - wall_from).normalize1()
            pos = wall_from
            while True:
                last = False
                if pos == wall_to:
                    last = True
                m[pos] = MapItem.wall
                # m.pprint()
                # walls.add(pos)
                pos += vel
                if last:
                    break

    m.pprint()
    ans = 0
    pos: Coord | None = None
    ready = False
    standing_y = m.origin.y + m.size.y - 1 + 2
    while True:
        try:
            if ready:
                break

            m[source] = MapItem.source
            if pos is None:
                ans += 1
                pos = source
                m[pos] = MapItem.sand
                continue

            check_poses = [pos + Coord(0, 1), pos + Coord(-1, 1), pos + Coord(1, 1)]
            for check_pos in check_poses:

                if level == 1 and check_pos not in m:
                    ready = True
                    break

                if level == 2:
                    if check_pos.y == standing_y:
                        m[check_pos] = MapItem.wall
                    if check_pos not in m:
                        m[check_pos] = MapItem.background

                if m[check_pos] == MapItem.background:
                    m[pos] = MapItem.background
                    m[check_pos] = MapItem.sand
                    pos = check_pos
                    break
            else:
                if level == 2 and pos == source:
                    break
                pos = None
                # m.pprint()
                # time.sleep(0.01)
        finally:
            pass
            # m.pprint()
            # time.sleep(0.01)
    m.pprint()
    print(ans - 1 if level == 1 else ans)


if __name__ == "__main__":
    solution(utils.get_level())
