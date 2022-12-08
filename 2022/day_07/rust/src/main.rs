use std::{
    env,
    error::Error,
    fs::File,
    io::Lines,
    io::{BufRead, BufReader},
    path::Path,
};

use anyhow::Result;
use regex::Regex;

struct Parser {
    file_item_re: Regex,
}

impl Parser {
    fn new() -> Self {
        return Self {
            file_item_re: Regex::new(r"^\d+").unwrap(),
        };
    }

    fn parse_dir(&self, lines: &mut Lines<BufReader<File>>) -> Vec<i64> {
        let mut subdirs = vec![0];
        while let Some(Ok(line)) = lines.next() {
            if line == "$ cd .." {
                break;
            } else if line.starts_with("$ cd") {
                let ds = self.parse_dir(lines);
                subdirs[0] += ds[0];
                subdirs.extend(ds);
            } else if let Some(c) = self.file_item_re.captures(&line) {
                subdirs[0] += c[0].parse::<i64>().expect("Could not parse file size!");
            }
        }
        subdirs
    }

    fn parse<P: AsRef<Path>>(&self, path: P) -> Result<Vec<i64>> {
        let f = File::open(path)?;
        let reader = BufReader::new(f);
        let mut lines = reader.lines();

        return Ok(self.parse_dir(&mut lines));
    }
}

fn solve_part1<P: AsRef<Path>>(path: P) -> Result<i64> {
    let dirs = Parser::new().parse(path)?;
    return Ok(dirs.into_iter().filter(|&n| n <= 100_000).sum());
}

fn solve_part2<P: AsRef<Path>>(path: P) -> Result<i64> {
    let dirs = Parser::new().parse(path)?;
    let min_size = 30_000_000 - 70_000_000 + dirs[0];
    let mut dirs: Vec<_> = dirs
        .into_iter()
        .filter(|&n| n >= min_size)
        .collect::<Vec<i64>>();
    dirs.sort();

    return Ok(dirs[0]);
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = env::args();
    let path = &args.nth(1).expect("Missing path param");
    println!("Part 1: {}", solve_part1(&path)?);
    println!("Part 2: {}", solve_part2(&path)?);
    Ok(())
}

#[cfg(test)]
mod test {
    use super::*;
    #[test]
    fn test_part1_sample() {
        let expected = 95437;
        assert_eq!(
            solve_part1("../sample.txt").expect("Should have been an i64"),
            expected
        );
    }

    #[test]
    fn test_part1_input() {
        let expected = 1_423_358;
        assert_eq!(
            solve_part1("../input.txt").expect("Should have been an i64"),
            expected
        );
    }

    #[test]
    fn test_part2_sample() {
        let expected = 24933642;
        assert_eq!(
            solve_part2("../sample.txt").expect("Should have been an i64"),
            expected
        );
    }

    #[test]
    fn test_part2_input() {
        let expected = 545729;
        assert_eq!(
            solve_part2("../input.txt").expect("Should have been an i64"),
            expected
        );
    }
}
