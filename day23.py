import functools
from collections import defaultdict
from typing import TypeAlias

import utils

N = 1000

Coord: TypeAlias = tuple[int, int]


def c_sum(a: Coord, b: Coord) -> Coord:
    return a[0] + b[0], a[1] + b[1]


def c_diff(a: Coord, b: Coord) -> Coord:
    return a[0] - b[0], a[1] - b[1]


def c_min(a: Coord, b: Coord) -> Coord:
    return min(a[0], b[0]), min(a[1], b[1])


def c_max(a: Coord, b: Coord) -> Coord:
    return max(a[0], b[0]), max(a[1], b[1])


def calc_rect(elves: set[Coord], to_print: bool = False):
    mn = functools.reduce(c_min, elves, (N, N))
    mx = c_sum(functools.reduce(c_max, elves, (0, 0)), (1, 1))
    rect = c_diff(mx, mn)
    if to_print:
        print(mn)
        for y in range(mn[0], mx[0]):
            for x in range(mn[1], mx[1]):
                if (y, x) in elves:
                    print("#", end="")
                else:
                    print(".", end="")
            print()
        print()
    return rect


def solution(level: int):
    # field: list[list[int]] = [[0 for _ in range(N)] for _ in range(N)]
    start_i = N // 2
    start_j = N // 2

    elves: set[Coord] = set()
    for i, line in enumerate(utils.input_reader()):
        for j, s in enumerate(line):
            if s == "#":
                # field[start_i + i][start_j + j] = 1
                elves.add((start_i + i, start_j + j))

    neighboring_tiles: list[Coord] = [
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1),
    ]
    neighboring_checks: list[tuple[list[Coord], Coord]] = [
        ([(-1, -1), (-1, 0), (-1, 1)], (-1, 0)),  # North
        ([(1, 1), (1, 0), (1, -1)], (1, 0)),  # South
        ([(1, -1), (0, -1), (-1, -1)], (0, -1)),  # West
        ([(-1, 1), (0, 1), (1, 1)], (0, 1)),  # East
    ]
    propositions: dict[Coord, list[Coord]] = defaultdict(list)
    _round = 0
    while True:
        _round += 1
        if level == 1 and _round > 10:
            break
        # Propositions
        propositions.clear()
        for elf in elves:
            any_neighbors = any(
                c_sum(elf, neighboring_tile) in elves
                for neighboring_tile in neighboring_tiles
            )
            if not any_neighbors:
                continue
            for tiles, vel in neighboring_checks:
                any_neighbors = any(
                    c_sum(elf, neighboring_tile) in elves for neighboring_tile in tiles
                )
                if not any_neighbors:
                    propositions[c_sum(elf, vel)].append(elf)
                    break

        # Moving
        if level == 2 and not propositions:
            break

        for proposition, proposition_list in propositions.items():
            if len(proposition_list) > 1:
                continue
            assert len(proposition_list) == 1
            elf_cur_pos = proposition_list[0]
            elves.remove(elf_cur_pos)
            elves.add(proposition)

        # Next round
        neighboring_checks = neighboring_checks[1:] + [neighboring_checks[0]]
        # calc_rect(elves, to_print=True)

    rect = calc_rect(elves, to_print=True)
    if level == 1:
        print(rect[0] * rect[1] - len(elves))
    else:
        print(_round)


def main(level: int):
    solution(level)


if __name__ == "__main__":
    main(utils.get_level())
