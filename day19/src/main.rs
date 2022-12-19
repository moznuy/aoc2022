use std::fs::File;
use std::io::{self, prelude::*, BufReader};
use std::path::Path;

use regex::Regex;

#[derive(Debug)]
struct Blueprint {
    number: i32,
    ore_ore: i32,
    clay_ore: i32,
    obsidian_ore: i32,
    obsidian_clay: i32,
    geode_ore: i32,
    geode_obsidian: i32,
    limit_ore: i32,
    limit_clay: i32,
    limit_obsidian: i32,
}

impl Blueprint {
    fn new(
        number: i32,
        ore_ore: i32,
        clay_ore: i32,
        obsidian_ore: i32,
        obsidian_clay: i32,
        geode_ore: i32,
        geode_obsidian: i32,
    ) -> Blueprint {
        Blueprint {
            number,
            ore_ore,
            clay_ore,
            obsidian_ore,
            obsidian_clay,
            geode_ore,
            geode_obsidian,
            limit_ore: *[ore_ore, clay_ore, obsidian_ore].iter().max().unwrap(),
            limit_clay: obsidian_clay,
            limit_obsidian: geode_obsidian,
        }
    }
}

fn solve(
    time_bidget: i32,
    robot_ore: i32,
    robot_clay: i32,
    robot_obsidian: i32,
    robot_geode: i32,
    ore: i32,
    clay: i32,
    obsidian: i32,
    geode: i32,
    could_ore: bool,
    could_clay: bool,
    could_obsidian: bool,
    // could_geode: bool,
    b: &Blueprint,
) -> i32 {
    let mut ans = geode;
    if time_bidget == 0 {
        return ans;
    }

    let can_ore = ore >= b.ore_ore;
    let can_clay = ore >= b.clay_ore;
    let can_obsidian = ore >= b.obsidian_ore && clay >= b.obsidian_clay;
    let can_geode = ore >= b.geode_ore && obsidian >= b.geode_obsidian;

    if can_geode {
        let partial = solve(
            time_bidget - 1,
            robot_ore,
            robot_clay,
            robot_obsidian,
            robot_geode + 1,
            ore + robot_ore - b.geode_ore,
            clay + robot_clay,
            obsidian + robot_obsidian - b.geode_obsidian,
            geode + robot_geode,
            false,
            false,
            false,
            b,
        );
        return ans.max(partial);
    }
    if can_ore && robot_ore < b.limit_ore && !could_ore {
        let partial = solve(
            time_bidget - 1,
            robot_ore + 1,
            robot_clay,
            robot_obsidian,
            robot_geode,
            ore + robot_ore - b.ore_ore,
            clay + robot_clay,
            obsidian + robot_obsidian,
            geode + robot_geode,
            false,
            false,
            false,
            b,
        );
        ans = ans.max(partial);
    }
    if can_clay && robot_clay < b.limit_clay && !could_clay {
        let partial = solve(
            time_bidget - 1,
            robot_ore,
            robot_clay + 1,
            robot_obsidian,
            robot_geode,
            ore + robot_ore - b.clay_ore,
            clay + robot_clay,
            obsidian + robot_obsidian,
            geode + robot_geode,
            false,
            false,
            false,
            b,
        );
        ans = ans.max(partial);
    }
    if can_obsidian && robot_obsidian < b.limit_obsidian && !could_obsidian {
        let partial = solve(
            time_bidget - 1,
            robot_ore,
            robot_clay,
            robot_obsidian + 1,
            robot_geode,
            ore + robot_ore - b.obsidian_ore,
            clay + robot_clay - b.obsidian_clay,
            obsidian + robot_obsidian,
            geode + robot_geode,
            false,
            false,
            false,
            b,
        );
        ans = ans.max(partial);
    }
    let partial = solve(
        time_bidget - 1,
        robot_ore,
        robot_clay,
        robot_obsidian,
        robot_geode,
        ore + robot_ore,
        clay + robot_clay,
        obsidian + robot_obsidian,
        geode + robot_geode,
        can_ore,
        can_clay,
        can_obsidian,
        b,
    );
    ans.max(partial)
}

fn main() -> io::Result<()> {
    let file = File::open(Path::new("..").join("input.txt"))?;
    let reader = BufReader::new(file);
    let re = Regex::new(r"\D+").unwrap();

    let bluprints: Vec<_> = reader
        .lines()
        .map(|line| {
            let numbers: Vec<_> = re
                .split(line.unwrap().as_str())
                .filter(|&s| !s.is_empty())
                .map(|s| s.parse::<i32>().unwrap())
                .collect();
            assert!(numbers.len() == 7);
            let b = Blueprint::new(
                numbers[0], numbers[1], numbers[2], numbers[3], numbers[4], numbers[5], numbers[6],
            );
            // println!("{:?}", b);
            b
        })
        .collect();
    let ans: i32 = bluprints
        .iter()
        .map(|b| {
            let solution: i32 = solve(24, 1, 0, 0, 0, 0, 0, 0, 0, false, false, false, b).into();
            // println!("{} {}", solution, b.number);
            solution * b.number
        })
        .sum();
    println!("{}", ans);
    let ans: i32 = (&bluprints[..3])
        .iter()
        .map(|b| {
            let solution: i32 = solve(32, 1, 0, 0, 0, 0, 0, 0, 0, false, false, false, b).into();
            // println!("{}", solution);
            solution
        })
        .product();
    print!("{}", ans);
    Ok(())
}
