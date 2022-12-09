import copy
import math
from contextlib import suppress
from typing import List
from typing import Mapping
from typing import Optional
from typing import Set
from typing import Tuple
from typing import TypeAlias

import utils

Coordinate: TypeAlias = Tuple[int, int]


def diagonal_distance(pos1: Coordinate, pos2: Coordinate) -> int:
    return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))


def sign_zero(n: int) -> int:
    if n == 0:
        return 0
    return n // abs(n)


def move_tail(head: Coordinate, tail: Coordinate) -> Optional[Coordinate]:
    diff = head[0] - tail[0], head[1] - tail[1]
    velocity = sign_zero(diff[0]), sign_zero(diff[1])
    return solve_velocity(tail, velocity)


def solve_tail(head: Coordinate, tail: Coordinate) -> Coordinate:
    distance = diagonal_distance(head, tail)
    if distance <= 1:
        return tail

    if distance == 2:
        return move_tail(head, tail)

    raise AssertionError


def solve_velocity(point: Coordinate, velocity: Coordinate) -> Coordinate:
    return point[0] + velocity[0], point[1] + velocity[1]


def recalc_min_max(
    pos: Coordinate, _min: Coordinate, _max: Coordinate
) -> Tuple[Coordinate, Coordinate]:
    return (min(_min[0], pos[0]), min(_min[1], pos[1])), (
        max(_max[0], pos[0]),
        max(_max[1], pos[1]),
    )


def print_map(
    head: Coordinate,
    tails: List[Coordinate],
    min_coord: Coordinate,
    max_coord: Coordinate,
    was: Optional[Set[Coordinate]] = None,
    # was_priority: bool = False,
):
    for y in range(max_coord[1], min_coord[1] - 1, -1):
        for x in range(min_coord[0], max_coord[0] + 1):
            # if was_priority and was and (x, y) in was:
            #     print("#", end="")
            #     continue
            if head[0] == x and head[1] == y:
                print("H", end="")
                continue
            try:
                index = tails.index((x, y))
                print(f"{index + 1}", end="")
                continue
            except ValueError:
                pass
            if x == 0 and y == 0:
                print("s", end="")
                continue
            if was and (x, y) in was:
                print("#", end="")
                continue
            print(".", end="")
        print()
    print()


# TODO: Nope, just write N^2 for simplicity
def solution(level: int):
    head = min_coord = max_coord = (0, 0)
    tails: List[Coordinate] = [(0, 0) for _ in range(1 if level == 1 else 9)]
    was: Set[Coordinate] = {tails[-1]}
    velocity_map: Mapping[str, Coordinate] = {
        "R": (1, 0),
        "U": (0, 1),
        "L": (-1, 0),
        "D": (0, -1),
    }

    # print_map(head, tail, min_coord, max_coord, was)
    for line in utils.input_reader():
        direction, steps = line.split()
        steps: int = int(steps)
        velocity = velocity_map[direction]

        for _ in range(steps):
            head = solve_velocity(head, velocity)
            tails.insert(0, head)
            for i in range(1, len(tails)):
                tails[i] = solve_tail(tails[i - 1], tails[i])
            tails = tails[1:]
            was.add(tails[-1])
            min_coord, max_coord = recalc_min_max(head, min_coord, max_coord)
        # print_map(head, tails, min_coord, max_coord, was)

    print("Final map:")
    print_map(head, tails, min_coord, max_coord, was)
    print(len(was))


if __name__ == "__main__":
    solution(utils.get_level())
