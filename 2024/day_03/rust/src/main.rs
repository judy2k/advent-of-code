use std::{
    error::Error,
    io::{self, Read},
};

use regex::Regex;

fn read_stdin() -> io::Result<String> {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;

    Ok(input)
}

fn solve_part1(input: &str) -> Result<i32, Box<dyn Error>> {
    let pattern = Regex::new(r"(mul)\((-?\d+),(-?\d+)\)")?;

    Ok(pattern
        .captures_iter(input)
        .map(|m| {
            let (_, [_funcname, op1, op2]) = m.extract();
            let op1: i32 = op1.parse().unwrap();
            let op2: i32 = op2.parse().unwrap();

            op1 * op2
        })
        .sum())
}

fn solve_part2(input: &str) -> Result<i32, Box<dyn Error>> {
    // The following regex has 3 options, each resulting in 3 captures
    // (even though with do and don't only the first capture will be non-empty.)
    let pattern = Regex::new(
        r#"(?x)    # Verbose regex
            (mul)\((-?\d+),(-?\d+)\)
            |(do)\(()()\)
            |(don't)\(()()\)"#,
    )
    .unwrap();
    Ok(pattern
        .captures_iter(input)
        .fold((true, 0), |(capturing, tally), m| {
            let (_, [funcname, op1, op2]) = m.extract();

            match funcname {
                "mul" if capturing => (
                    true,
                    tally + op1.parse::<i32>().unwrap() * op2.parse::<i32>().unwrap(),
                ),
                "do" if !capturing => (true, tally),
                "don't" if capturing => (false, tally),
                _ => (capturing, tally),
            }
        })
        .1)
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_stdin()?;

    println!("Part 1: {}", solve_part1(&input)?);
    println!("Part 2: {}", solve_part2(&input)?);

    Ok(())
}
