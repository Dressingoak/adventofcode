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

const fn is_vowel(c: char) -> bool {
    match c {
        'a' | 'e' | 'i' | 'o' | 'u' => true,
        _ => false,
    }
}

const fn is_bad_pair(first: char, second: char) -> bool {
    match (first, second) {
        ('a', 'b') | ('c', 'd') | ('p', 'q') | ('x', 'y') => true,
        _ => false,
    }
}

fn is_nice_string(string: &str) -> bool {
    let mut vowels = 0;
    let mut repeats = false;

    let mut chars = string.chars();
    let mut chars_next = string.chars().skip(1);
    loop {
        if let Some(c) = chars.next() {
            if is_vowel(c) {
                vowels += 1;
            }
            if let Some(n) = chars_next.next() {
                if n == c {
                    repeats = true;
                }
                if is_bad_pair(c, n) {
                    return false;
                }
            } else {
                break;
            }
        } else {
            break;
        }
    }
    repeats && (vowels >= 3)
}

fn main() -> Result<()> {
    let filename = env::args().nth(1).expect("Filename should be set");
    let mut nice = 0;
    for line in read_lines(&filename)? {
        let string = line?;
        if is_nice_string(&string) {
            nice += 1;
        }
    }
    println!("Dec 5, part 1: {}", nice);
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p1() {
        assert_eq!(true, is_nice_string("ugknbfddgicrmopn"));
        assert_eq!(true, is_nice_string("aaa"));
        assert_eq!(false, is_nice_string("jchzalrnumimnmhp"));
        assert_eq!(false, is_nice_string("haegwjzuvuyypxyu"));
        assert_eq!(false, is_nice_string("dvszwmarrgswjxmb"));
    }
}
