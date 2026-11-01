use std::{fs::File, io::Read};
use std::env;

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
            _ => panic!("Unexpected character")
        }
    }
    floor
}

fn main() -> std::io::Result<()> {
    let file = env::args().nth(1).expect("Filename should be set");
    let input = read_input(&file)?;
    println!("Dec 1, part 1: {}",p1(&input));
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
}
