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

    let mut total = 0;
    for m in pattern.captures_iter(input) {
        let (_, [_funcname, op1, op2]) = m.extract();
        let op1: i32 = op1.parse()?;
        let op2: i32 = op2.parse()?;

        total += op1 * op2;
    }

    Ok(total)
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_stdin()?;

    println!("Part 1: {}", solve_part1(&input)?);
    // println!("Part 2: {}", solve_part2(&input)?);

    Ok(())
}
