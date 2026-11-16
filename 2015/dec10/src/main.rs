use anyhow::{Context, Result};
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

fn read_line<P>(filename: P) -> Result<String>
where
    P: AsRef<Path>,
{
    let path = filename.as_ref();
    let line = read_lines(path)
        .with_context(|| format!("failed to open {}", path.display()))?
        .next()
        .with_context(|| format!("{} is empty", path.display()))??;
    Ok(line)
}

fn look_and_say(seq: &str) -> String {
    let mut out = String::new();
    let mut cur = None;
    let mut len = 0;
    for c in seq.chars() {
        match (c, cur) {
            (_, None) => {
                cur = Some(c);
                len = 1;
            }
            (cn, Some(cp)) if cn == cp => {
                len += 1;
            }
            (cn, Some(cp)) if cn != cp => {
                out.push_str(&format!("{len}{cp}"));
                cur = Some(cn);
                len = 1;
            }
            _ => unreachable!(),
        }
    }
    if let Some(cl) = cur {
        out.push_str(&format!("{len}{cl}"));
    }
    out
}

fn main() -> Result<()> {
    let filename = env::args().nth(1).expect("Filename should be set");
    let mut seq = read_line(&filename)?;
    for _ in 0..40 {
        seq = look_and_say(&seq);
    }
    println!("Dec 10, part 1: {}", seq.len());
    for _ in 0..10 {
        seq = look_and_say(&seq);
    }
    println!("Dec 10, part 2: {}", seq.len());
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p1() {
        assert_eq!(look_and_say("1"), "11".to_string());
        assert_eq!(look_and_say("11"), "21".to_string());
        assert_eq!(look_and_say("21"), "1211".to_string());
        assert_eq!(look_and_say("1211"), "111221".to_string());
        assert_eq!(look_and_say("111221"), "312211".to_string());
    }
}
