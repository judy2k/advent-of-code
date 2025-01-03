use std::{
    error::Error,
    io::{self, BufRead},
};

enum ReportResult {
    FailAt(usize),
    Pass,
}

use ReportResult::{FailAt, Pass};

impl ReportResult {
    fn is_pass(self) -> bool {
        match self {
            Self::Pass => true,
            _ => false,
        }
    }
}

fn sign(i: i32) -> i32 {
    if i == 0 {
        0
    } else {
        i / i.abs()
    }
}

fn check_levels(ints: &[i32], up: i32) -> ReportResult {
    for i in 0..(ints.len() - 1) {
        let diff = ints[i + 1] - ints[i];

        if sign(diff) != up {
            return FailAt(i);
        }

        let abs_diff = diff.abs();
        if abs_diff > 3 || abs_diff < 1 {
            return FailAt(i);
        }
    }
    return Pass;
}

fn direction(levels: &[i32]) -> i32 {
    sign((0..4).map(|i| sign(levels[i + 1] - levels[i])).sum())
}

fn skip_copy(input: &[i32], skip: usize) -> Vec<i32> {
    let mut without_i = Vec::with_capacity(input.len() - 1);
    without_i.extend(&input[..skip]);
    without_i.extend(&input[skip + 1..]);
    without_i
}

fn parse_levels(line: &str) -> Vec<i32> {
    line.trim().split(" ").map(|t| t.parse().unwrap()).collect()
}

fn solve_part_1(lines: &Vec<String>) -> i32 {
    lines
        .into_iter()
        .map(|line| parse_levels(&line))
        .map(|levels| check_levels(&levels, direction(&levels)).is_pass() as i32)
        .sum()
}

fn solve_part_2(lines: &Vec<String>) -> i32 {
    lines
        .into_iter()
        .map(|line| parse_levels(&line))
        .map(|levels| {
            let direction = direction(&levels);
            match check_levels(&levels, direction) {
                Pass => 1,
                FailAt(i) if check_levels(&skip_copy(&levels, i), direction).is_pass() => 1,
                FailAt(i) if check_levels(&skip_copy(&levels, i + 1), direction).is_pass() => 1,
                _ => 0,
            }
        })
        .sum()
}

fn main() -> Result<(), Box<dyn Error>> {
    let stdin = io::stdin();

    let input: Vec<String> = stdin.lock().lines().map(Result::unwrap).collect();

    println!("Part 1: {}", solve_part_1(&input));
    println!("Part 2: {}", solve_part_2(&input));

    Ok(())
}
