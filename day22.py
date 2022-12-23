from __future__ import annotations
import dataclasses
import functools
import pprint
from typing import Callable
from typing import cast
from typing import Generator
from typing import NamedTuple
from typing import TypeAlias

import utils


Coord: TypeAlias = tuple[int, int]
Check: TypeAlias = Callable[[Coord, Coord], int | None]


def c_sum(a: Coord, b: Coord) -> Coord:
    return a[0] + b[0], a[1] + b[1]


def c_diff(a: Coord, b: Coord) -> Coord:
    return a[0] - b[0], a[1] - b[1]


def c_norm(a: Coord) -> Coord:
    return a[0] // abs(a[0]) if a[0] != 0 else 0, a[1] // abs(a[1]) if a[1] != 0 else 0


def c_mult(a: Coord, n: int) -> Coord:
    return a[0] * n, a[1] * n


def c_axis_dist(a: Coord, b: Coord) -> int:
    if a[0] == b[0]:
        return abs(a[1] - b[1])
    if a[1] == b[1]:
        return abs(a[0] - b[0])
    raise ValueError("Not parallel to axes")


def next_command(s: str) -> Generator[int | str, None, None]:
    n: int | None = None
    for c in s:
        if c.isnumeric():
            if n is None:
                n = 0
            n *= 10
            n += int(c)
            continue
        if n is not None:
            yield n
            n = None
        yield c
    if n is not None:
        yield n


def solution1(field, width, height, walk, rotation_map, facing_map, pos, vel):
    for command in next_command(walk):
        if isinstance(command, str):
            rotation = rotation_map[command]
            vel = rotation[0] * vel[1], rotation[1] * vel[0]
            continue
        for step in range(command):
            try_pos = pos[0], pos[1]
            while True:
                try_pos = c_sum(try_pos, vel)
                if try_pos[0] >= height:
                    try_pos = (0, try_pos[1])
                if try_pos[0] < 0:
                    try_pos = (height - 1, try_pos[1])
                if try_pos[1] >= width:
                    try_pos = (try_pos[0], 0)
                if try_pos[1] < 0:
                    try_pos = (try_pos[0], width - 1)
                if field[try_pos[0]][try_pos[1]] > 0:
                    break
            if field[try_pos[0]][try_pos[1]] == 1:
                pos = try_pos
                continue
            if field[try_pos[0]][try_pos[1]] == 2:
                break

    ans = 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + facing_map[vel]
    print(ans)


@dataclasses.dataclass
class Face:
    number: int
    edges: Edges


class Edges(NamedTuple):
    up: Edge
    right: Edge
    down: Edge
    left: Edge


@dataclasses.dataclass
class Edge:
    check: Check
    partner: Edge | None
    reversed: bool | None
    parent: Face | None
    start: Coord
    finish: Coord
    vector_inbound: Coord


def is_face(field, i, j, k) -> bool:
    face: bool | None = None
    for y in range(k):
        for x in range(k):
            c0 = i * k + y
            c1 = j * k + x
            if face is None:
                face = field[c0][c1] > 0
                continue
            assert face is (field[c0][c1] > 0)
    return face


def check(
    cur_pos: Coord, check_pos: Coord, start: Coord, finish: Coord, vector_inbound: Coord
) -> int | None:
    horizontal = start[0] == finish[0]
    dc = 1 if horizontal else 0  # Different coordinate
    sc = 0 if horizontal else 1  # Same coordinate

    if not (start[dc] <= cur_pos[dc] <= finish[dc]):
        return None
    if not (start[dc] <= check_pos[dc] <= finish[dc]):
        return None
    if not (start[sc] == cur_pos[sc] == finish[sc]):
        return None
    if not (start[sc] == check_pos[sc] + vector_inbound[sc] == finish[sc]):
        return None
    return cur_pos[dc] - start[dc]


def check_all(faces, cur_pos, next_pos) -> tuple[Edge, int] | None:
    for face in faces.values():
        for edge in face.edges:
            crossing = edge.check(cur_pos, next_pos)
            if crossing is not None:
                return edge, crossing


def solution2(field, width, height, walk, rotation_map, facing_map, pos, vel):
    faces: dict[int, Face] = {}

    k = 50  # 4
    assert width % k == 0
    assert height % k == 0
    face_number = 0
    for i in range(height // k):
        for j in range(width // k):
            if not is_face(field, i, j, k):
                continue

            edges = Edges(
                *(
                    Edge(
                        check=cast(
                            Check,
                            functools.partial(
                                check,
                                start=start,
                                finish=finish,
                                vector_inbound=vector_inbound,
                            ),
                        ),
                        partner=None,
                        reversed=None,
                        parent=None,
                        start=start,
                        finish=finish,
                        vector_inbound=vector_inbound,
                    )
                    for start, finish, vector_inbound in (
                        ((i * k, j * k), (i * k, (j + 1) * k - 1), (1, 0)),
                        (
                            (i * k, (j + 1) * k - 1),
                            ((i + 1) * k - 1, (j + 1) * k - 1),
                            (0, -1),
                        ),
                        (
                            ((i + 1) * k - 1, j * k),
                            ((i + 1) * k - 1, (j + 1) * k - 1),
                            (-1, 0),
                        ),
                        ((i * k, j * k), ((i + 1) * k - 1, j * k), (0, 1)),
                    )
                )
            )

            face_number += 1
            new_face = Face(number=face_number, edges=edges)
            for edge in edges:
                edge.parent = new_face
            faces[face_number] = new_face

    assert len(faces) == 6

    # hardcoded_solution: list[(int, int, int, int, bool)] = [
    #     (1, 0, 2, 0, True),
    #     (1, 1, 6, 1, True),
    #     (1, 2, 4, 0, False),
    #     (1, 3, 3, 0, False),
    #     (2, 1, 3, 3, False),
    #     (2, 2, 5, 2, True),
    #     (2, 3, 6, 2, True),
    #     (3, 1, 4, 3, False),
    #     (3, 2, 5, 3, True),
    #     (4, 1, 6, 0, True),
    #     (4, 2, 5, 0, False),
    #     (5, 1, 6, 3, False),
    # ]
    hardcoded_solution: list[(int, int, int, int, bool)] = [
        (1, 0, 6, 3, False),
        (1, 1, 2, 3, False),
        (1, 2, 3, 0, False),
        (1, 3, 4, 3, True),
        (2, 0, 6, 2, False),
        (2, 1, 5, 1, True),
        (2, 2, 3, 1, False),
        (3, 2, 5, 0, False),
        (3, 3, 4, 0, False),
        (4, 1, 5, 3, False),
        (4, 2, 6, 0, False),
        (5, 2, 6, 1, False),
    ]

    for s in hardcoded_solution:
        ff, fe, tf, te, r = s  # From face, from edge, to face, to edge, reversed
        faces[ff].edges[fe].partner = faces[tf].edges[te]
        faces[ff].edges[fe].reversed = r
        faces[tf].edges[te].partner = faces[ff].edges[fe]
        faces[tf].edges[te].reversed = r

    for face_no, face in faces.items():
        for edge_no, edge in enumerate(face.edges):
            assert (
                edge.partner is not None
            ), f"Face {face_no} edge {edge_no} has no partner"
            assert (
                edge.reversed is not None
            ), f"Face {face_no} edge {edge_no} has no partner"

    try_pos: Coord
    crossed_edge: Edge
    crossing: int
    try_vel: Coord | None

    for command in next_command(walk):
        if isinstance(command, str):
            rotation = rotation_map[command]
            vel = rotation[0] * vel[1], rotation[1] * vel[0]
            continue

        for step in range(command):
            try_pos = c_sum(pos, vel)

            crossed = check_all(faces, pos, try_pos)
            try_vel = None
            if crossed is not None:
                crossed_edge, crossing = crossed
                arrived_edge = crossed_edge.partner
                arrived_edge_tangent = c_norm(
                    c_diff(arrived_edge.finish, arrived_edge.start)
                )
                arrived_edge_tangent_t = (
                    crossing
                    if not crossed_edge.reversed
                    else c_axis_dist(arrived_edge.finish, arrived_edge.start) - crossing
                )
                try_pos = c_sum(
                    arrived_edge.start,
                    c_mult(arrived_edge_tangent, arrived_edge_tangent_t),
                )
                try_vel = arrived_edge.vector_inbound

            if field[try_pos[0]][try_pos[1]] == 1:
                pos = try_pos
                if try_vel:
                    vel = try_vel
                continue
            if field[try_pos[0]][try_pos[1]] == 2:
                break
            assert False

    ans = 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + facing_map[vel]
    print(ans)
    # 178171
    # 162096


def solution(level: int):
    lines = [line for line in utils.input_reader(chars="\n")]
    walk = lines[-1]
    lines = lines[:-2]

    width = max(map(len, lines))
    height = len(lines)
    field: list[list[int]] = [[0 for _ in range(width)] for _ in range(height)]
    for y, line in enumerate(lines):
        s: str
        for x, s in enumerate(line):
            if s.isspace():
                continue
            if s == ".":
                field[y][x] = 1
                continue
            if s == "#":
                field[y][x] = 2

    pos: Coord = (0, field[0].index(1))
    vel: Coord = (0, 1)
    rotation_map: dict[str, Coord] = {
        "R": (1, -1),
        "L": (-1, 1),
    }
    facing_map: dict[Coord, int] = {
        (0, 1): 0,
        (1, 0): 1,
        (0, -1): 2,
        (-1, 0): 3,
    }
    # pprint.pprint(field)
    if level == 1:
        solution1(field, width, height, walk, rotation_map, facing_map, pos, vel)
    else:
        solution2(field, width, height, walk, rotation_map, facing_map, pos, vel)


def main(level: int):
    solution(level)


if __name__ == "__main__":
    main(utils.get_level())
