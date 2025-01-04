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

    Ok(pattern.captures_iter(input).map(|m| {
        let (_, [_funcname, op1, op2]) = m.extract();
        let op1: i32 = op1.parse().unwrap();
        let op2: i32 = op2.parse().unwrap();

        op1 * op2
    }).sum())
}

fn solve_part2(input: &str) -> Result<i32, Box<dyn Error>> {
    let pattern = Regex::new(r"(mul)\((-?\d+),(-?\d+)\)|(do)\(\)|(don't)\(\)")?;

    let mut capturing = true;
    let mut tally = 0;
    for m in pattern.captures_iter(input) {
        let funcname = m.get(1).or_else(|| m.get(4).or_else(||m.get(5))).unwrap().as_str();

        match funcname {
            "mul" if capturing => {
                let op1: i32 = m.get(2).unwrap().as_str().parse()?;
                let op2: i32 = m.get(3).unwrap().as_str().parse()?;
                tally += op1 * op2;
            },
            "do" => capturing = true,
            "don't" => capturing = false,
            _ => {},
        }
    }

    Ok(tally)
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_stdin()?;

    println!("Part 1: {}", solve_part1(&input)?);
    println!("Part 2: {}", solve_part2(&input)?);

    Ok(())
}
