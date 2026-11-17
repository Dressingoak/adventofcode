use anyhow::Result;
use std::env;
use utils::read_line;

fn sum(json: &str) -> i32 {
    let mut sum = 0;
    let mut sign = false;
    let mut value: Option<i32> = None;
    for c in json.chars() {
        match c {
            '-' => {
                sign = true;
            }
            '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' => {
                let digit = ((c as u8) - 48) as i32;
                match &mut value {
                    Some(v) => {
                        *v *= 10;
                        *v += digit;
                    }
                    None => value = Some(digit),
                }
            }
            _ => {
                if let Some(v) = value {
                    sum += if !sign { v } else { -v };
                    sign = false;
                    value = None;
                }
            }
        }
    }
    if let Some(v) = value {
        sum += if !sign { v } else { -v };
    }
    sum
}

fn main() -> Result<()> {
    let filename = env::args().nth(1).expect("Filename should be set");
    let json = read_line(&filename)?;
    let sum = sum(&json);
    println!("Dec 12, part 1: {sum}");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p1() {
        assert_eq!(sum("[1,2,3]"), 6);
        assert_eq!(sum("{\"a\":2,\"b\":4}"), 6);
        assert_eq!(sum("[[[3]]]"), 3);
        assert_eq!(sum("{\"a\":{\"b\":4},\"c\":-1}"), 3);
        assert_eq!(sum("{\"a\":[-1,1]}"), 0);
        assert_eq!(sum("[-1,{\"a\":1}]"), 0);
        assert_eq!(sum("[]"), 0);
        assert_eq!(sum("{}"), 0);
    }
}
