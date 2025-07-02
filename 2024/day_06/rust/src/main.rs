use std::{
    collections::HashSet, default, fmt::{self, Display, Formatter}, io
};

struct Grid {
    cells: Vec<Vec<char>>,
    blocks: HashSet<(usize, usize)>,
    width: usize,
    height: usize,
}

impl Grid {
    fn new(cells: Vec<Vec<char>>) -> Self {
        let width = cells.len();
        let height = cells[0].len();

        Self {
            cells,
            blocks: Default::default(),
            width,
            height,
        }
    }

    fn read_from_stdin() -> Self {
        Self::new({
            io::stdin()
                .lines()
                .map(|line| line.unwrap().chars().collect())
                .collect()
        })
    }

    fn inside(&self, pos: (usize, usize)) -> bool {
        let (row, col) = pos;
        row < self.height && col < self.width 
    }

    fn blocked(&self, pos: (usize, usize)) -> bool {
        return self.inside(pos) && self.blocks.contains(&pos);
    }
}

impl Display for Grid {
    fn fmt(&self, f: &mut Formatter) -> fmt::Result {
        for row in &self.cells {
            for cell in row {
                write!(f, "{}", cell)?
            }
            writeln!(f, "")?;
        }
        Ok(())
    }
}

fn main() {
    let grid = Grid::read_from_stdin();

    println!("{}", grid);
}

fn rotate(current: (isize, isize)) -> (isize, isize) {
    (current.1, -current.0)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rotate() {
        assert_eq!(rotate((-1, 0)), (0, 1));
        assert_eq!(rotate((0, 1)), (1, 0));
        assert_eq!(rotate((1, 0)), (0, -1));
        assert_eq!(rotate((0, -1)), (-1, 0));
    }
}
