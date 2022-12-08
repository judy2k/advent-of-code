use std::env;
use std::error::Error;
use std::fs::File;
use std::io::Lines;
use std::io::{BufRead, BufReader};
use std::path::Path;

use anyhow::Result;
use lazy_static::lazy_static;
use regex::Regex;

lazy_static! {
    static ref FILE_ITEM_RE: Regex = Regex::new(r"^\d+").unwrap();
}

fn parse_dir(lines: &mut Lines<BufReader<File>>) -> Vec<i64> {
    let mut subdirs = vec![0];
    while let Some(Ok(line)) = lines.next() {
        if line == "$ cd .." {
            break;
        } else if line.starts_with("$ cd") {
            let ds = parse_dir(lines);
            subdirs[0] += ds[0];
            subdirs.extend(ds);
        } else if let Some(c) = FILE_ITEM_RE.captures(&line) {
            subdirs[0] += c[0].parse::<i64>().expect("Could not parse file size!");
        }
    }
    subdirs
}

fn parse<P: AsRef<Path>>(path: P) -> Result<Vec<i64>> {
    let f = File::open(path)?;
    let reader = BufReader::new(f);
    let mut lines = reader.lines();

    Ok(parse_dir(&mut lines))
}

fn solve_part1(dirs: Vec<i64>) -> Result<i64> {
    Ok(dirs.into_iter().filter(|&n| n <= 100_000).sum())
}

fn solve_part2(dirs: Vec<i64>) -> Result<i64> {
    let min_size = 30_000_000 - 70_000_000 + dirs[0];
    let mut dirs = dirs
        .into_iter()
        .filter(|&n| n >= min_size)
        .collect::<Vec<i64>>();
    dirs.sort();

    Ok(dirs[0])
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = env::args();
    let path = &args.nth(1).expect("Missing path param");
    let dirs = parse(path)?;

    println!("Part 1: {}", solve_part1(dirs.clone())?);
    println!("Part 2: {}", solve_part2(dirs)?);
    Ok(())
}

#[cfg(test)]
mod test {
    use super::*;
    #[test]
    fn test_part1_sample() {
        let dirs = parse("../sample.txt").expect("Could not read file.");
        let expected = 95437;
        assert_eq!(
            solve_part1(dirs).expect("Should have been an i64"),
            expected
        );
    }

    #[test]
    fn test_part1_input() {
        let dirs = parse("../input.txt").expect("Could not read file.");
        let expected = 1_423_358;
        assert_eq!(
            solve_part1(dirs).expect("Should have been an i64"),
            expected
        );
    }

    #[test]
    fn test_part2_sample() {
        let dirs = parse("../sample.txt").expect("Could not read file.");
        let expected = 24933642;
        assert_eq!(
            solve_part2(dirs).expect("Should have been an i64"),
            expected
        );
    }

    #[test]
    fn test_part2_input() {
        let dirs = parse("../input.txt").expect("Could not read file.");
        let expected = 545729;
        assert_eq!(
            solve_part2(dirs).expect("Should have been an i64"),
            expected
        );
    }
}
