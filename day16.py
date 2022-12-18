import itertools
import re
from typing import TypeAlias

import utils

Mask: TypeAlias = int


def traverse(
    cache: dict[Mask, int],
    vertex: str,
    index_matrix: dict[tuple[str, str], int],
    flow_list: list[tuple[int, str]],
    masks: dict[str, Mask],
    was: Mask,
    pressure: int = 0,
    step: int = 0,
) -> dict[Mask, int]:
    cache[was] = max(cache.get(was, 0), pressure)

    for flow, next_vertex in flow_list:
        new_step = step - index_matrix[(vertex, next_vertex)] - 1
        if masks[next_vertex] & was or new_step <= 0:
            continue
        traverse(
            cache,
            next_vertex,
            index_matrix,
            flow_list,
            masks,
            was | masks[next_vertex],
            pressure + flow * new_step,
            new_step,
        )
    return cache


def solution(level):
    vertex_regex = re.compile(r"[A-Z]{2}")
    flow_regex = re.compile(r"\d+")
    index_matrix: dict[tuple[str, str], int] = {}
    vertex: set[str] = set()
    flow_list: list[tuple[int, str]] = []

    for line in utils.input_reader():
        origin, *dests = vertex_regex.findall(line)
        flows = flow_regex.findall(line)
        assert len(flows) == 1
        flow = int(flows[0])
        vertex.add(origin)
        index_matrix[(origin, origin)] = 0
        flow_list.append((flow, origin))
        for dest in dests:
            index_matrix[(origin, dest)] = 1

    flow_list.sort(reverse=True)
    flow_list = list(filter(lambda ii: ii[0] > 0, flow_list))
    masks: dict[str, Mask] = {flow[1]: 1 << i for i, flow in enumerate(flow_list)}

    # Floyd Warshall
    for k in vertex:
        for i in vertex:
            for j in vertex:
                if (i, k) in index_matrix and (k, j) in index_matrix:
                    index_matrix[(i, j)] = min(
                        index_matrix.setdefault((i, j), 10000),
                        index_matrix[(i, k)] + index_matrix[(k, j)],
                    )

    if level == 1:
        cache = traverse(
            {}, "AA", index_matrix, flow_list, masks, was=0, pressure=0, step=30
        )
        print(max(v for v in cache.values()))
    elif level == 2:
        cache = traverse(
            {}, "AA", index_matrix, flow_list, masks, was=0, pressure=0, step=26
        )
        print(
            max(
                v1 + v2
                for (m1, v1), (m2, v2) in itertools.product(
                    cache.items(), cache.items()
                )
                if not m1 & m2
            )
        )
    else:
        assert False


def main(level: int):
    solution(level)


if __name__ == "__main__":
    main(1)
