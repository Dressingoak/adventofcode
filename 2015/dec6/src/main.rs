use anyhow::{Result, bail};
use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::num::ParseIntError;
use std::path::Path;
use std::str::FromStr;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

#[derive(Clone, Copy)]
struct Point<T> {
    x: T,
    y: T,
}

impl<T> TryFrom<&str> for Point<T>
where
    T: FromStr<Err = ParseIntError>,
{
    type Error = anyhow::Error;

    fn try_from(value: &str) -> Result<Self> {
        let mut iter = value.split(',').map(|v| {
            let v: Result<T, ParseIntError> = v.parse();
            v
        });
        if let (Some(Ok(x)), Some(Ok(y))) = (iter.next(), iter.next()) {
            if iter.next().is_none() {
                return Ok(Point { x, y });
            } else {
                bail!("Expected exactly 2 values")
            }
        } else {
            bail!("Expected exactly 2 values")
        }
    }
}

enum Action {
    Toggle,
    TurnOn,
    TurnOff,
}

fn main() -> Result<()> {
    let filename = env::args().nth(1).expect("Filename should be set");
    let mut grid = [[false; 1000]; 1000];
    for line in read_lines(&filename)? {
        let string = line?;
        let split: Vec<&str> = string.split_ascii_whitespace().collect();
        let (action, p1, p2) = match split[..] {
            ["turn", "on", p1, "through", p2] => (Action::TurnOn, p1.try_into()?, p2.try_into()?),
            ["turn", "off", p1, "through", p2] => (Action::TurnOff, p1.try_into()?, p2.try_into()?),
            ["toggle", p1, "through", p2] => (Action::Toggle, p1.try_into()?, p2.try_into()?),
            _ => bail!("Found unexpected pattern: {string}"),
        };
        let Point::<usize> { x: x1, y: y1 } = p1;
        let Point::<usize> { x: x2, y: y2 } = p2;
        for x in x1..=x2 {
            for y in y1..=y2 {
                let entry = &mut grid[y][x];
                match action {
                    Action::TurnOn => *entry = true,
                    Action::Toggle => *entry = !*entry,
                    Action::TurnOff => *entry = false,
                }
            }
        }
    }
    let lit: u32 = grid
        .iter()
        .map(|row| row.iter().map(|&x| if x { 1 } else { 0 }).sum::<u32>())
        .sum();

    println!("Dec 6, part 1: {}", lit);
    Ok(())
}
