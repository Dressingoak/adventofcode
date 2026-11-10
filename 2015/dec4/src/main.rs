mod md5;

use anyhow::{Result, bail};
use md5::md5;
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

fn p1(key: &str) -> usize {
    let mut i = 0;
    loop {
        let test = format!("{}{}", key, i);
        let hash = md5(test.as_bytes());
        let repr = format!("{:032x}", hash);
        if &repr[..5] == "00000" {
            break i;
        }
        i += 1;
    }
}

fn main() -> Result<()> {
    let filename = env::args().nth(1).expect("Filename should be set");
    if let Some(line) = read_lines(&filename)?.next() {
        let l = line?;
        println!("Dec 4, part 1: {}", p1(&l));
    } else {
        bail!("Could not read line")
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p1() {
        assert_eq!(609043, p1("abcdef"));
    }
}
