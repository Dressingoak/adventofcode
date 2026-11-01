use anyhow::{Result, anyhow};
use std::env;
use std::{fs::File, io::Read};

fn read_input(file: &str) -> std::io::Result<String> {
    let mut file = File::open(file)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents.trim().to_string())
}

fn p1(data: &str) -> i32 {
    let mut floor = 0;
    for c in data.chars() {
        match c {
            '(' => floor += 1,
            ')' => floor -= 1,
            _ => panic!("Unexpected character"),
        }
    }
    floor
}

fn p2(data: &str) -> Result<usize> {
    let mut floor = 0i32;
    for (i, c) in data.chars().enumerate() {
        match c {
            '(' => floor += 1,
            ')' => floor -= 1,
            _ => panic!("Unexpected character"),
        }
        if floor == -1 {
            return Ok(i + 1);
        }
    }
    Err(anyhow!("Did not find the basement floor"))
}

fn main() -> Result<()> {
    let file = env::args().nth(1).expect("Filename should be set");
    let input = read_input(&file)?;
    println!("Dec 1, part 1: {}", p1(&input));
    println!("Dec 1, part 2: {}", p2(&input)?);
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p1() {
        assert_eq!(0, p1("(())"));
        assert_eq!(0, p1("()()"));

        assert_eq!(3, p1("((("));
        assert_eq!(3, p1("(()(()("));

        assert_eq!(3, p1("))((((("));

        assert_eq!(-1, p1("())"));
        assert_eq!(-1, p1("))("));

        assert_eq!(-3, p1(")))"));
        assert_eq!(-3, p1(")())())"));
    }

    #[test]
    fn test_p2() {
        assert_eq!(1, p2(")").unwrap());
        assert_eq!(5, p2("()())").unwrap());
    }
}
