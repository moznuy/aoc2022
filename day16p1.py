import pprint
import re

import utils

TTT = 0


def traverse(
    vertex: str,
    was: set[str],
    index_matrix: dict[tuple[str, str], int],
    flow_list: list[tuple[int, str]],
    flow: int = 0,
    pressure: int = 0,
    step: int = 0,
) -> tuple[int | None, list[str]]:
    global TTT
    TTT += 1

    if step == 30:
        return pressure, [vertex]
    if step > 30:
        return None, []

    pressure_m = pressure
    step_m = step
    flow_m = flow
    max_pressure30 = 0
    max_vertexes = []
    for f, v in flow_list:
        if v in was:
            continue
        if v == vertex:
            continue

        pressure = pressure_m
        step = step_m
        flow = flow_m
        minutes = index_matrix[(vertex, v)] + 1  # index_matrix to reach, 1 to open
        pressure += flow * minutes
        step += minutes
        flow += f

        if step > 30:
            continue

        was.add(v)
        try_pressure, try_vertexes = traverse(
            v, was, index_matrix, flow_list, flow, pressure, step
        )
        was.discard(v)

        if try_pressure is not None:
            # max_pressure30 = max(max_pressure30, try_pressure)
            if try_pressure > max_pressure30:
                max_pressure30 = try_pressure
                max_vertexes = try_vertexes

    # ...., spent 30 minutes with this bug
    # no_moving_pressure = pressure + (30 - step) * flow
    no_moving_pressure = pressure_m + (30 - step_m) * flow_m

    # return max(no_moving_pressure, max_pressure30)
    if no_moving_pressure > max_pressure30:
        return no_moving_pressure, [vertex]
    return max_pressure30, [vertex] + max_vertexes


def solution(level):
    vertex_regex = re.compile(r"[A-Z]{2}")
    flow_regex = re.compile(r"\d+")
    index_matrix: dict[tuple[str, str], int] = {}
    vertex: set[str] = set()
    flow_list: list[tuple[int, str]] = []
    # flow_map: dict[str, int] = {}

    for line in utils.input_reader():
        origin, *dests = vertex_regex.findall(line)
        flows = flow_regex.findall(line)
        assert len(flows) == 1
        flow = int(flows[0])
        vertex.add(origin)
        index_matrix[(origin, origin)] = 0
        flow_list.append((flow, origin))
        # flow_map[origin] = flow
        for dest in dests:
            index_matrix[(origin, dest)] = 1
        # print(origin, flow, dests)

    flow_list.sort(reverse=True)
    flow_list = list(filter(lambda ii: ii[0] > 0, flow_list))

    # Floyd Warshall
    for k in vertex:
        for i in vertex:
            for j in vertex:
                if (i, k) in index_matrix and (k, j) in index_matrix:
                    index_matrix[(i, j)] = min(
                        index_matrix.setdefault((i, j), 10000),
                        index_matrix[(i, k)] + index_matrix[(k, j)],
                    )

    pprint.pprint(index_matrix)
    pprint.pprint(flow_list)
    ans = traverse("AA", {"AA"}, index_matrix, flow_list, flow=0, pressure=0, step=0)
    print(ans, TTT)


if __name__ == "__main__":
    solution(utils.get_level())
