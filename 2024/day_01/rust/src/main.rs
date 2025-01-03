use std::error::Error;
use std::io;
use std::io::prelude::*;

use counter::Counter;

fn solve_part_1(lines: &[String]) -> i32 {
    let (mut a, mut b): (Vec<_>, Vec<_>) = lines
        .iter()
        .map(|line| {
            let items: Vec<i32> = line
                .trim()
                .splitn(2, "   ")
                .map(|t| t.parse().unwrap())
                .collect();
            (items[0], items[1])
        })
        .unzip();
    a.sort();
    b.sort();

    a.into_iter()
        .zip(b)
        .map(|(a, b)| (a - b).abs())
        .sum::<i32>()
}

fn solve_part_2(lines: &[String]) -> i32 {
    let (a, b): (Vec<_>, Counter<_>) = lines
        .iter()
        .map(|line| {
            let items: Vec<usize> = line
                .trim()
                .splitn(2, "   ")
                .map(str::parse)
                .map(Result::unwrap)
                .collect();
            (items[0], items[1])
        })
        .unzip();
    a.into_iter()
        .map(|ref k| k * b.get(k).unwrap_or(&0))
        .sum::<usize>() as i32
}

fn main() -> Result<(), Box<dyn Error>> {
    let stdin = io::stdin();

    let input: Vec<String> = stdin.lock().lines().map(Result::unwrap).collect();

    println!("Part 1: {}", solve_part_1(&input));
    println!("Part 2: {}", solve_part_2(&input));

    Ok(())
}
