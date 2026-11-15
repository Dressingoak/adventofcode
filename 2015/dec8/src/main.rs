use anyhow::Result;
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

fn count_in_memory(string: &str) -> usize {
    let mut n_in_memory = 0;
    let mut escape = false;
    let mut hex_left = 0;
    for c in string.chars() {
        match c {
            '\\' => {
                if escape {
                    escape = false;
                    n_in_memory += 1
                } else {
                    escape = true;
                }
            }
            '"' => {
                if escape {
                    escape = false;
                    n_in_memory += 1
                }
            }
            'x' if escape => {
                hex_left = 2;
            }
            _ if hex_left == 2 => {
                hex_left -= 1;
            }
            _ if hex_left == 1 => {
                n_in_memory += 1;
                hex_left = 0;
                escape = false;
            }
            _ => n_in_memory += 1,
        }
    }
    n_in_memory
}

fn count_excess_chars(string: &str) -> usize {
    string.len() - count_in_memory(string)
}

fn count_encoded(string: &str) -> usize {
    let mut size = 2;
    for c in string.chars() {
        match c {
            '\\' | '"' => size += 2,
            _ => size += 1,
        }
    }
    size
}

fn count_excess_encoded(string: &str) -> usize {
    count_encoded(string) - string.len()
}

fn main() -> Result<()> {
    let filename = env::args().nth(1).expect("Filename should be set");
    let mut n = 0;
    let mut m = 0;
    for line in read_lines(&filename)? {
        let l = line?;
        n += count_excess_chars(&l);
        m += count_excess_encoded(&l);
    }
    println!("Dec 8, part 1: {n}");
    println!("Dec 8, part 2: {m}");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p1() {
        for (s, in_memory, size) in [
            ("\"\"", 0, 2),
            ("\"abc\"", 3, 5),
            ("\"aaa\\\"aaa\"", 7, 10),
            ("\"\\x27\"", 1, 6),
        ] {
            assert_eq!(size, s.len());
            assert_eq!(in_memory, count_in_memory(s));
        }
    }

    #[test]
    fn test_p2() {
        for (s, size, encoded) in [
            ("\"\"", 2, 6),
            ("\"abc\"", 5, 9),
            ("\"aaa\\\"aaa\"", 10, 16),
            ("\"\\x27\"", 6, 11),
        ] {
            assert_eq!(size, s.len());
            assert_eq!(encoded, count_encoded(s));
        }
    }
}
