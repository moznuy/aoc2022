import operator
import queue
from typing import cast
from typing import TypeAlias

import utils

Coord: TypeAlias = tuple[int, int, int]


def is_touching(a: Coord, b: Coord) -> bool:
    assert len(a) == len(b)
    zero = sum(abs(a[i] - b[i]) == 0 for i in range(len(a)))
    one = sum(abs(a[i] - b[i]) == 1 for i in range(len(a)))
    return zero == 2 and one == 1


def inside_box(c: Coord, mn: Coord, mx: Coord) -> bool:
    assert len(c) == len(mn) == len(mx)
    return all(mn[i] <= c[i] <= mx[i] for i in range(len(c)))


def coord_sum(a: Coord, b: Coord) -> Coord:
    assert len(a) == len(b)
    return cast(Coord, tuple(a[i] + b[i] for i in range(len(a))))


def solution1(cubes: set[Coord]) -> None:
    ans = 0
    for i, cube in enumerate(cubes):
        touch = 0
        for j, test_cube in enumerate(cubes):
            if j <= i:
                continue
            if is_touching(cube, test_cube):
                touch += 2
        assert 0 <= touch <= 12
        ans += 6 - touch
    print(ans)


def solution2(cubes: set[Coord]) -> None:
    mn = cast(
        Coord, tuple(min(cubes, key=operator.itemgetter(i))[i] - 2 for i in range(3))
    )
    mx = cast(
        Coord, tuple(max(cubes, key=operator.itemgetter(i))[i] + 2 for i in range(3))
    )

    q: queue.Queue[Coord] = queue.Queue()
    q.put(mn)

    ans = 0
    checks: list[Coord] = [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, -1),
    ]
    was: set[Coord] = set()
    was.add(mn)

    while not q.empty():
        cur = q.get()

        for check in checks:
            check_cube = coord_sum(cur, check)

            if check_cube in cubes:
                ans += 1
                continue

            if check_cube in was:
                continue

            if not inside_box(check_cube, mn, mx):
                continue

            was.add(check_cube)
            q.put(check_cube)

    print(ans)


def solution(level: int) -> None:
    cubes: set[Coord] = {
        cast(Coord, tuple(map(int, line.split(",")))) for line in utils.input_reader()
    }
    if level == 1:
        solution1(cubes)
    elif level == 2:
        solution2(cubes)


if __name__ == "__main__":
    solution(utils.get_level())
