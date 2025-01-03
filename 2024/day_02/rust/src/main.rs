use std::{
    error::Error,
    io::{self, BufRead},
};

enum ReportResult {
    FailAt(usize),
    Pass,
}

fn sign(i: i32) -> i32 {
    if i == 0 {
        0
    } else {
        i / i.abs()
    }
}

fn check_levels(ints: &[i32], up: i32) -> ReportResult {
    // println!("Checking Levels: {:?}", ints);
    for i in 0..(ints.len() - 1) {
        let a = ints[i];
        let b = ints[i + 1];

        // println!("{} == {}?", dir(a, b), up);
        if sign(b - a) != up {
            return ReportResult::FailAt(i);
        }

        let diff = (b - a).abs();
        if diff > 3 || diff < 1 {
            // println!("Failing at {i}");
            return ReportResult::FailAt(i);
        }
    }
    return ReportResult::Pass;
}

fn solve_part_1(lines: &Vec<String>) -> i32 {
    let mut tally = 0;

    for line in lines {
        let levels: Vec<i32> = line.trim().split(" ").map(|t| t.parse().unwrap()).collect();
        if let ReportResult::Pass = check_levels(&levels, direction(&levels)) {
            tally += 1;
        }
    }

    tally
}

fn direction(levels: &[i32]) -> i32 {
    let mut tally = 0;
    for i in 0..4 {
        let diff = levels[i + 1] - levels[i];
        if diff != 0 {
            tally += diff / diff.abs();
        }
    }

    if tally == 0 {
        0
    } else {
        tally / tally.abs()
    }
}

fn skip_copy(input: &[i32], skip: usize) -> Vec<i32> {
    let mut without_i = Vec::with_capacity(input.len() - 1);
    without_i.extend(&input[..skip]);
    without_i.extend(&input[skip + 1..]);
    without_i
}

fn solve_part_2(lines: &Vec<String>) -> i32 {
    let mut tally = 0;

    for line in lines {
        let levels: Vec<i32> = line.trim().split(" ").map(|t| t.parse().unwrap()).collect();
        let direction = direction(&levels);
        match check_levels(&levels, direction) {
            ReportResult::Pass => tally += 1,
            ReportResult::FailAt(i) => {
                if let ReportResult::Pass = check_levels(&skip_copy(&levels, i), direction) {
                    tally += 1
                } else if let ReportResult::Pass =
                    check_levels(&skip_copy(&levels, i + 1), direction)
                {
                    tally += 1
                }
            }
        }
    }

    tally
}

fn main() -> Result<(), Box<dyn Error>> {
    let stdin = io::stdin();

    let input: Vec<String> = stdin.lock().lines().map(Result::unwrap).collect();

    println!("Part 1: {}", solve_part_1(&input));
    println!("Part 2: {}", solve_part_2(&input));

    Ok(())
}
