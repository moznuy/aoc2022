import copy
import queue
from typing import TypeAlias

import utils

Coord: TypeAlias = tuple[int, int]


def c_sum(a: Coord, b: Coord) -> Coord:
    return a[0] + b[0], a[1] + b[1]


def frozen_field(field: list[list[int]]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(cell for cell in row) for row in field)


def precalc_blizzards(field: list[list[list[int]]], width: int, height: int) -> int:
    assert len(field) == 1
    step = 0
    cache = {frozen_field(field[0]): step}
    while True:
        step += 1

        new_field = copy.deepcopy(field[-1])
        for y in range(height):
            for x in range(width):
                if new_field[y][x] > 0:
                    new_field[y][x] = 0

        for y in range(height):
            for x in range(width):
                if field[-1][y][x] <= 0:
                    continue
                for wind_dir, wind_vel in zip(
                    (1, 2, 4, 8), ((0, 1), (1, 0), (0, -1), (-1, 0))
                ):
                    check_pos = c_sum((y, x), wind_vel)
                    if check_pos[0] == height - 1:
                        check_pos = 1, check_pos[1]
                    if check_pos[0] == 0:
                        check_pos = height - 2, check_pos[1]
                    if check_pos[1] == width - 1:
                        check_pos = check_pos[0], 1
                    if check_pos[1] == 0:
                        check_pos = check_pos[0], width - 2

                    if not (
                        field[-1][y][x] & wind_dir
                        and new_field[check_pos[0]][check_pos[1]] >= 0
                    ):
                        continue
                    assert not (new_field[check_pos[0]][check_pos[1]] & wind_dir)
                    new_field[check_pos[0]][check_pos[1]] |= wind_dir

        # pprint.pprint(new_field)
        key = frozen_field(new_field)
        found = cache.setdefault(key, step)
        if found < step:
            assert found == 0
            return step
        field.append(new_field)


def sim(
    start: Coord,
    end: Coord,
    field: list[list[list[int]]],
    height: int,
    period: int,
    step: int = 0,
) -> int:
    ans = 0
    q: queue.Queue[tuple[Coord, int]] = queue.Queue()
    q.put((start, step))
    was: set[tuple[Coord, int]] = {(start, step)}
    while not q.empty():
        pos, step = q.get()
        if pos == end:
            ans = step
            break
        for vel in ((0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)):
            check_pos = c_sum(pos, vel)
            check_step = step + 1
            key = check_pos, check_step % period
            if key in was:
                continue
            if check_pos[0] < 0 or check_pos[0] >= height:
                continue
            if field[check_step % period][check_pos[0]][check_pos[1]] != 0:
                continue
            was.add(key)
            q.put((check_pos, check_step))
    return ans


def solution(level: int) -> None:
    lines = [line for line in utils.input_reader()]
    width = len(lines[0])
    height = len(lines)
    field: list[list[list[int]]] = [[[0 for _ in range(width)] for _ in range(height)]]
    input_mapping = {
        ".": 0,
        "#": -1,
        ">": 1,
        "v": 2,
        "<": 4,
        "^": 8,
    }

    for y in range(height):
        for x in range(width):
            field[0][y][x] = input_mapping[lines[y][x]]

    start = 0, field[0][0].index(0)
    end = height - 1, field[0][-1].index(0)
    # pprint.pprint(field)
    # print(start, end)
    period = precalc_blizzards(field, width, height)
    assert len(field) == period
    print(f"Period: {period}")

    if level == 1:
        print(sim(start, end, field, height, period))
    else:
        step = sim(start, end, field, height, period)
        step = sim(end, start, field, height, period, step)
        step = sim(start, end, field, height, period, step)
        print(step)


def main(level: int) -> None:
    solution(level)


if __name__ == "__main__":
    main(utils.get_level())
