use anyhow::{Result, bail};
use std::collections::HashSet;
use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn p1(steps: &str) -> Result<usize> {
    let mut visited = HashSet::new();
    let (mut x, mut y) = (0, 0);
    visited.insert((x, y));
    for c in steps.chars() {
        let (h, v) = match c {
            '^' => (0, 1),
            '>' => (1, 0),
            'v' => (0, -1),
            '<' => (-1, 0),
            c => bail!("Unexpected character: '{}'", c)
        };
        x += h;
        y += v;
        visited.insert((x, y));
    }
    Ok(visited.len())
}


fn main() -> Result<()> {
    let filename = env::args().nth(1).expect("Filename should be set");
    let houses;
    if let Some(line) = read_lines(&filename)?.next() {
        let l = line?;
        houses = p1(&l)?;
    } else {
        bail!("Could not read line")
    }
    println!("Dec 3, part 1: {}", houses);
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p1() {
        assert_eq!(2, p1(">").unwrap());
        assert_eq!(4, p1("^>v<").unwrap());
        assert_eq!(2, p1("^v^v^v^v^v").unwrap());
    }

}
