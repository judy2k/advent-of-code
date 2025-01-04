use std::{
    error::Error,
    io::{self, BufRead},
};

use ReportResult::{FailAt, Pass};

enum ReportResult {
    FailAt(usize),
    Pass,
}

impl ReportResult {
    fn is_pass(self) -> bool {
        match self {
            Pass => true,
            _ => false,
        }
    }
}

fn check_levels(ints: &[i32], up: i32, skip: Option<usize>) -> ReportResult {
    for i in 0..(ints.len() - 1) {
        if Some(i) != skip {
            let diff = if Some(i + 1) == skip {
                if i + 2 < ints.len() {
                    ints[i + 2] - ints[i]
                } else {
                    continue;
                }
            } else {
                ints[i + 1] - ints[i]
            };

            if diff.signum() != up {
                return FailAt(i);
            }

            let abs_diff = diff.abs();
            if abs_diff > 3 || abs_diff < 1 {
                return FailAt(i);
            }
        }
    }
    return Pass;
}

fn direction(levels: &[i32]) -> i32 {
    ((0..4)
        .map(|i| (levels[i + 1] - levels[i]).signum())
        .sum::<i32>())
    .signum()
}

fn parse_levels(line: &str) -> Vec<i32> {
    line.trim().split(" ").map(|t| t.parse().unwrap()).collect()
}

fn solve_part_1(lines: &Vec<String>) -> i32 {
    lines
        .into_iter()
        .map(|line| parse_levels(&line))
        .map(|levels| check_levels(&levels, direction(&levels), None).is_pass() as i32)
        .sum()
}

fn solve_part_2(lines: &Vec<String>) -> i32 {
    lines
        .into_iter()
        .map(|line| parse_levels(&line))
        .map(|levels| {
            let direction = direction(&levels);
            match check_levels(&levels, direction, None) {
                Pass => 1,
                FailAt(i) if check_levels(&levels, direction, Some(i)).is_pass() => 1,
                FailAt(i) if check_levels(&levels, direction, Some(i + 1)).is_pass() => 1,
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
