use std::{error::Error, io};

struct Grid {
    lines: Vec<Vec<char>>,
    width: usize,
    height: usize,
}

impl Grid {
    fn new(lines: Vec<Vec<char>>) -> Self {
        let width = lines.len();
        let height = lines[0].len();

        Self {
            lines,
            width,
            height,
        }
    }

    fn read_from_stdin() -> Result<Self, io::Error> {
        let lines: Vec<Vec<char>> = io::stdin()
            .lines()
            .collect::<Result<Vec<_>, _>>()?
            .into_iter()
            .map(|line| line.chars().collect::<Vec<char>>())
            .collect();

        Ok(Self::new(lines))
    }

    fn get(&self, row: usize, col: usize) -> Option<char> {
        self.lines.get(row).and_then(|line| line.get(col)).copied()
    }

    fn test_xmas_1(&self, start_row: usize, start_col: usize, f: fn(i32) -> (i32, i32)) -> bool {
        let xmas = vec!['X', 'M', 'A', 'S'];
        for i in 0..4 {
            let (rowmod, colmod) = f(i);
            if self.get(
                (start_row as i32 + rowmod) as usize,
                (start_col as i32 + colmod) as usize,
            ) != Some(xmas[i as usize])
            {
                return false;
            }
        }

        true
    }

    fn test_xmas_2(&self, start_row: usize, start_col: usize) -> bool {
        if start_row >= 1
            && start_row < self.height - 1
            && start_col >= 1
            && start_col < self.width - 1
        {
            let opt1 = (Some('M'), Some('S'));
            let opt2 = (Some('S'), Some('M'));

            let d1 = (
                self.get(start_row - 1, start_col - 1),
                self.get(start_row + 1, start_col + 1),
            );
            let d2 = (
                self.get(start_row - 1, start_col + 1),
                self.get(start_row + 1, start_col - 1),
            );
            return (d1 == opt1 || d1 == opt2) && (d2 == opt1 || d2 == opt2);
        }

        false
    }
}

fn solve_part1(grid: &Grid) -> Result<i32, Box<dyn Error>> {
    let mut tally = 0;
    for row in 0..grid.width {
        for col in 0..grid.height {
            if grid.get(row, col) == Some('X') {
                // Try up:
                if row >= 3 {
                    if grid.test_xmas_1(row, col, |i| (-i, 0)) {
                        tally += 1
                    }

                    // Up left:
                    if col >= 3 && grid.test_xmas_1(row, col, |i| (-i, -i)) {
                        tally += 1
                    }

                    // Up right:
                    if col < grid.width - 3 && grid.test_xmas_1(row, col, |i| (-i, i)) {
                        tally += 1
                    }
                }

                // Try down:
                if row < grid.height - 3 {
                    if grid.test_xmas_1(row, col, |i| (i, 0)) {
                        tally += 1
                    }

                    // Down left:
                    if col >= 3 && grid.test_xmas_1(row, col, |i| (i, -i)) {
                        tally += 1
                    }

                    // Down right:
                    if col < grid.width - 3 && grid.test_xmas_1(row, col, |i| (i, i)) {
                        tally += 1
                    }
                }

                // Try left:
                if col >= 3 && grid.test_xmas_1(row, col, |i| (0, -i)) {
                    tally += 1
                }

                // Try right:
                if col < grid.width - 3 && grid.test_xmas_1(row, col, |i| (0, i)) {
                    tally += 1
                }
            }
        }
    }

    Ok(tally)
}

fn solve_part2(grid: &Grid) -> Result<i32, Box<dyn Error>> {
    let mut tally = 0;
    for row in 0..grid.width {
        for col in 0..grid.height {
            if grid.get(row, col) == Some('A') && grid.test_xmas_2(row, col) {
                tally += 1
            }
        }
    }
    Ok(tally)
}

fn main() -> Result<(), Box<dyn Error>> {
    let grid = Grid::read_from_stdin()?;
    println!("Part 1: {}", solve_part1(&grid)?);
    println!("Part 2: {}", solve_part2(&grid)?);

    Ok(())
}
