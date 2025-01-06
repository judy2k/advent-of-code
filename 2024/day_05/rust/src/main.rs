use std::{cmp::Ordering::{self, *}, collections::HashSet, error::Error, io};

struct SortRules {
    rules: HashSet<(u32, u32)>,
}

impl SortRules {
    fn new() -> Self {
        Self {
            rules: Default::default(),
        }
    }

    fn add_rule(&mut self, a: u32, b: u32) {
        self.rules.insert((a, b));
    }

    fn sorter(&self, a: &u32, b: &u32) -> Ordering {
        if self.rules.contains(&(*a, *b)) {
            Less
        } else if self.rules.contains(&(*b, *a)) {
            Greater
        } else {
            Equal
        }
    }
}

fn solve_part1(sort_rules: &SortRules, lines: &Vec<String>) -> Result<u32, Box<dyn Error>> {
    let mut tally = 0;
    for line in lines {
        let ns: Vec<u32> = line.split(',').map(str::parse).collect::<Result<_, _>>()?;
        if ns.iter().is_sorted_by(|a, b| sort_rules.sorter(*a, *b) == Less) {
            tally += ns[ns.len() / 2];
        }
    }
    Ok(tally)
}

fn solve_part2(sort_rules: &SortRules, lines: &Vec<String>) -> Result<u32, Box<dyn Error>> {
    let mut tally = 0;
    for line in lines {
        let mut ns: Vec<u32> = line.split(',').map(str::parse).collect::<Result<_, _>>()?;
        if !ns.iter().is_sorted_by(|a, b| sort_rules.sorter(*a, *b) == Less) {
            ns.sort_by(|a, b| sort_rules.sorter(a, b));
            tally += ns[ns.len() / 2];
        }
    }
    Ok(tally)
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut sort_rules = SortRules::new();
    for line in io::stdin()
        .lines()
        .map(Result::unwrap)
        .take_while(|line| !line.is_empty())
    {
        if let Some((a, b)) = line.split_once('|') {
            sort_rules.add_rule(a.parse()?, b.parse()?);
        }
    }
    let lines: Vec<String> = io::stdin().lines().map(Result::unwrap).collect();

    println!("Part 1: {}", solve_part1(&sort_rules, &lines)?);
    println!("Part 2: {}", solve_part2(&sort_rules, &lines)?);

    Ok(())
}
