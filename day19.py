"""
Just don't look please
"""
import dataclasses
import functools
import multiprocessing
import operator
import re
import struct

import tqdm

import utils


TTT = 0


@dataclasses.dataclass
class Blueprint:
    number: int
    ore_ore: int
    clay_ore: int
    obsidian_ore: int
    obsidian_clay: int
    geode_ore: int
    geode_obsidian: int
    limit_ore: int = 0
    limit_clay: int = 0
    limit_obsidian: int = 0


def solve(
    minutes_remaining: int,
    robot_ore: int,
    robot_clay: int,
    robot_obsidian: int,
    robot_geode: int,
    ore: int,
    clay: int,
    obsidian: int,
    geode: int,
    could1: bool,
    could2: bool,
    could3: bool,
    could4: bool,
    cache: dict,
    b: Blueprint,
) -> int:
    global TTT
    TTT += 1

    key = int.from_bytes(
        struct.pack(
            "bbbbbhhhhbbbb",
            minutes_remaining,
            robot_ore,
            robot_clay,
            robot_obsidian,
            robot_geode,
            ore,
            clay,
            obsidian,
            geode,
            could1,
            could2,
            could3,
            could4,
        ),
        byteorder="little",
    )
    if key in cache:
        return cache[key]

    ans = geode
    # robot_ore == 1 and robot_clay == 4 and robot_obsidian == 2 and robot_geode == 1 and minutes_remaining == 6
    if minutes_remaining == 0:
        cache[key] = geode
        return geode

    # # FIXME: this is just to make it fit memory and some amount of time )
    # # FIXME: won't work in general case
    # if robot_ore > 6 or robot_clay > 10 or robot_obsidian > 10 or robot_geode > 10:
    #     cache[key] = geode
    #     return 0

    can1 = False
    can2 = False
    can3 = False
    can4 = False

    # ifs
    if ore >= b.ore_ore:
        can1 = True
    if ore >= b.clay_ore:
        can2 = True
    if ore >= b.obsidian_ore and clay >= b.obsidian_clay:
        can3 = True
    if ore >= b.geode_ore and obsidian >= b.geode_obsidian:
        can4 = True

    if ore >= b.geode_ore and obsidian >= b.geode_obsidian and not could4:
        partial = solve(
            minutes_remaining - 1,
            robot_ore,
            robot_clay,
            robot_obsidian,
            robot_geode + 1,
            ore + robot_ore - b.geode_ore,
            clay + robot_clay,
            obsidian + robot_obsidian - b.geode_obsidian,
            geode + robot_geode,
            False,
            False,
            False,
            False,
            cache,
            b,
        )
        ans = max(ans, partial)
        cache[key] = ans
        return ans
    if ore >= b.ore_ore and robot_ore < b.limit_ore and not could1:
        partial = solve(
            minutes_remaining - 1,
            robot_ore + 1,
            robot_clay,
            robot_obsidian,
            robot_geode,
            ore + robot_ore - b.ore_ore,
            clay + robot_clay,
            obsidian + robot_obsidian,
            geode + robot_geode,
            False,
            False,
            False,
            False,
            cache,
            b,
        )
        ans = max(ans, partial)
    if ore >= b.clay_ore and robot_clay < b.limit_clay and not could2:
        partial = solve(
            minutes_remaining - 1,
            robot_ore,
            robot_clay + 1,
            robot_obsidian,
            robot_geode,
            ore + robot_ore - b.clay_ore,
            clay + robot_clay,
            obsidian + robot_obsidian,
            geode + robot_geode,
            False,
            False,
            False,
            False,
            cache,
            b,
        )
        ans = max(ans, partial)
    if ore >= b.obsidian_ore and robot_obsidian < b.limit_obsidian and clay >= b.obsidian_clay and not could3:
        partial = solve(
            minutes_remaining - 1,
            robot_ore,
            robot_clay,
            robot_obsidian + 1,
            robot_geode,
            ore + robot_ore - b.obsidian_ore,
            clay + robot_clay - b.obsidian_clay,
            obsidian + robot_obsidian,
            geode + robot_geode,
            False,
            False,
            False,
            False,
            cache,
            b,
        )
        ans = max(ans, partial)

    # No buying
    partial = solve(
        minutes_remaining - 1,
        robot_ore,
        robot_clay,
        robot_obsidian,
        robot_geode,
        ore + robot_ore,
        clay + robot_clay,
        obsidian + robot_obsidian,
        geode + robot_geode,
        can1,
        can2,
        can3,
        can4,
        cache,
        b,
    )
    ans = max(ans, partial)
    cache[key] = ans
    return ans


def solver1(b: Blueprint):
    func = functools.partial(
        solve, 24, 1, 0, 0, 0, 0, 0, 0, 0, False, False, False, False, {}
    )
    result = func(b)
    return result * b.number


def solver2(b: Blueprint):
    func = functools.partial(
        solve, 32, 1, 0, 0, 0, 0, 0, 0, 0, False, False, False, False, {}
    )
    result = func(b)
    print(result)
    return result


def solution(level):
    global TTT
    blueprints = [
        Blueprint(*map(int, filter(None, re.split(r"\D+", line))))
        for line in utils.input_reader()
    ]
    for blueprint in blueprints:
        blueprint.limit_ore = max(blueprint.ore_ore, blueprint.clay_ore, blueprint.obsidian_ore, blueprint.geode_ore)
        blueprint.limit_clay = max(blueprint.obsidian_clay, 0)
        blueprint.limit_obsidian = max(blueprint.geode_obsidian, 0)

    print(solver2(blueprints[0]), TTT)
    TTT = 0
    print(solver2(blueprints[1]), TTT)
    TTT = 0
    print(solver2(blueprints[2]), TTT)
    return

    if level == 1:
        with multiprocessing.Pool(10) as pool:
            ans = sum(
                tqdm.tqdm(
                    pool.imap_unordered(solver1, blueprints), total=len(blueprints)
                )
            )

    if level == 2:
        with multiprocessing.Pool(3) as pool:
            ans = functools.reduce(
                operator.mul,
                tqdm.tqdm(pool.imap_unordered(solver2, blueprints[:3]), total=3),
            )

    # ans = sum(map(solver, blueprints[:5]))
    print(ans, TTT)
    # 1427
    # :5 37 119881070
    #    37 108168361
    #    37   6894488

    # 26 30206937
    # 26 24548024

    # 27 23478313
    # 27  1411907
    # 5 5662351
    #  5 785830
    # 6 4296694
    #  6 597786


def main(level: int):
    solution(level)


if __name__ == "__main__":
    main(1)
