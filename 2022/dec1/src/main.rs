use std::fs::File;
use std::io::{self, prelude::*, BufReader};
use std::path::Path;

fn calculate<P: AsRef<Path>>(path: P) -> io::Result<u32> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut cur: u32 = 0;
    let mut max: u32 = 0;

    for line in reader.lines() {
        match line?.trim() {
            "" => {
                if cur >= max {
                    max = cur;
                }
                cur = 0;
            },
            s => { cur += s.parse::<u32>().unwrap() },
        }
    }

    Ok(max)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p1() {
        assert_eq!(24000, calculate("../test.txt").unwrap());
    }

}

fn main() {
    println!("Dec 1, part 1: {}", calculate("input.txt").unwrap());
}
