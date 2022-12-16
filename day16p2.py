"""
FIXME: JUST NO...... Please fix me!
"""
import copy
import multiprocessing
import operator
import re

import tqdm

# noinspection PyUnresolvedReferences
import istarmap
import utils

LAST = 26
POOL: multiprocessing.Pool


def current_flow(was: set[str], flow_list: list[tuple[int, str]]):
    return sum(map(operator.itemgetter(0), filter(lambda f: f[1] in was, flow_list)))


def traverse(
    v1: str,
    t1: int,
    v2: str,
    t2: int,
    was: set[str],
    gone_to: set[str],
    index_matrix: dict[tuple[str, str], int],
    flow_list: list[tuple[int, str]],
    pressure: int = 0,
    step: int = 0,
) -> int:
    global POOL

    cf = current_flow(was, flow_list)
    pressure += cf * 1
    if step == LAST:
        return pressure

    if t1 > 0 and t2 > 0:
        max_step = min(t1, t2, LAST - step)
        pressure += cf * (max_step - 1)
        return traverse(v1, t1 - max_step, v2, t2 - max_step, was, gone_to, index_matrix, flow_list, pressure, step + max_step)

    if t1 == 0 and t2 > 0:
        only_arrived = v1 not in was
        if only_arrived:
            was.add(v1)
        cf_stayed = current_flow(was, flow_list)
        stayed_pressure = pressure + cf_stayed * (LAST - step)

        max_res = 0
        other_res = 0
        zero_iterations = True
        for flow in filter(lambda f: f[1] not in gone_to, flow_list):
            zero_iterations = False
            to = flow[1]
            time = index_matrix[(v1, to)]
            gone_to.add(to)

            max_step = min(t2, time, LAST - step)
            pressure_t = pressure + cf_stayed * (max_step - 1)
            res = traverse(to, time - max_step + 1, v2, t2 - max_step, was, gone_to, index_matrix, flow_list, pressure_t, step + max_step)
            max_res = max(max_res, res)

            gone_to.discard(to)

        if zero_iterations:
            max_step = min(t2, LAST - step)
            pressure += cf_stayed * (max_step - 1)
            other_res = traverse(v1, 0, v2, t2 - max_step, was, gone_to, index_matrix, flow_list, pressure, step + max_step)
        if only_arrived:
            was.discard(v1)
        return max(max_res, other_res, stayed_pressure)

    if t2 == 0 and t1 > 0:
        only_arrived = v2 not in was
        if only_arrived:
            was.add(v2)
        cf_stayed = current_flow(was, flow_list)
        stayed_pressure = pressure + cf_stayed * (LAST - step)

        max_res = 0
        other_res = 0
        zero_iterations = True
        for flow in filter(lambda f: f[1] not in gone_to, flow_list):
            zero_iterations = False
            to = flow[1]
            time = index_matrix[(v2, to)]
            gone_to.add(to)

            max_step = min(t1, time, LAST - step)
            pressure_t = pressure + cf_stayed * (max_step - 1)
            res = traverse(v1, t1 - max_step, to, time - max_step + 1, was, gone_to, index_matrix, flow_list, pressure_t, step + max_step)
            max_res = max(max_res, res)

            gone_to.discard(to)

        if zero_iterations:
            max_step = min(t1, LAST - step)
            pressure += cf_stayed * (max_step - 1)
            other_res = traverse(v1, t1 - max_step, v2, 0, was, gone_to, index_matrix, flow_list, pressure, step + max_step)
        if only_arrived:
            was.discard(v2)
        return max(max_res, other_res, stayed_pressure)

    if step == 0:
        args = []
        lll = list(filter(lambda f: f[1] not in gone_to, flow_list))
        for i, flow1 in enumerate(lll):
            for j, flow2 in enumerate(lll):
                if j <= i:
                    continue
                to1 = flow1[1]
                to2 = flow2[1]
                time1 = index_matrix[(v1, to1)]
                time2 = index_matrix[(v2, to2)]
                gone_to.add(to1)
                gone_to.add(to2)

                max_step = min(time1, time2, LAST - step)
                args.append(
                    (to1, time1 - max_step + 1, to2, time2 - max_step + 1, copy.deepcopy(was), copy.deepcopy(gone_to), copy.deepcopy(index_matrix), copy.deepcopy(flow_list), 0, step + max_step)
                )

                gone_to.discard(to2)
                gone_to.discard(to1)

        results = [result for result in tqdm.tqdm(POOL.istarmap_unordered(traverse, args), total=len(args))]
        result = max(results)
        return result
    else:
        assert t1 == 0 and t2 == 0
        only_arrived1 = v1 not in was
        only_arrived2 = v2 not in was
        if only_arrived1:
            was.add(v1)
        if only_arrived2:
            was.add(v2)
        cf_stayed = current_flow(was, flow_list)
        stayed_pressure = pressure + cf_stayed * (LAST - step)

        max_res = 0
        for flow1 in filter(lambda f: f[1] not in gone_to, flow_list):
            for flow2 in filter(lambda f: f[1] not in gone_to, flow_list):
                if flow1 == flow2:
                    continue
                to1 = flow1[1]
                to2 = flow2[1]
                time1 = index_matrix[(v1, to1)]
                time2 = index_matrix[(v2, to2)]
                gone_to.add(to1)
                gone_to.add(to2)

                max_step = min(time1, time2, LAST - step)
                pressure_t = pressure + cf_stayed * (max_step - 1)
                res = traverse(to1, time1 - max_step + 1, to2, time2 - max_step + 1, was, gone_to, index_matrix, flow_list, pressure_t, step + max_step)
                max_res = max(max_res, res)

                gone_to.discard(to2)
                gone_to.discard(to1)

        if only_arrived2:
            was.remove(v2)
        if only_arrived1:
            was.remove(v1)
        return max(max_res, stayed_pressure)


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
                    index_matrix[(i, j)] = min(index_matrix.setdefault((i, j), 10000), index_matrix[(i, k)] + index_matrix[(k, j)])

    # pprint.pprint(index_matrix)
    # pprint.pprint(flow_list)
    processes = 24
    with multiprocessing.Pool(processes) as pool:
        global POOL
        POOL = pool
        ans = traverse(v1="AA", t1=0, v2="AA", t2=0, was={"AA"}, gone_to={"AA"}, index_matrix=index_matrix, flow_list=flow_list, pressure=0, step=0)
    print(ans)


if __name__ == "__main__":
    solution(utils.get_level())
