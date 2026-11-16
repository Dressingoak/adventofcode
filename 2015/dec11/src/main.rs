use anyhow::{Context, Result, bail};
use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::{env, fmt};

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

#[derive(Debug, PartialEq, Eq)]
struct Password {
    chars: [u8; 8],
}

impl Password {
    fn increment_unchecked(&mut self) {
        for i in (0..8).rev() {
            if self.chars[i] == 25 {
                self.chars[i] = 0;
            } else {
                self.chars[i] += 1;
                return;
            }
        }
        self.chars = [0; 8];
    }

    fn has_chain(&self) -> bool {
        self.chars.windows(3).any(|x| match x[..] {
            [a, b, c] if (a + 1 == b) && (b + 1 == c) => true,
            _ => false,
        })
    }

    fn has_no_disallowed(&self) -> bool {
        // 8 == 'i' as char - 97
        // 14 == 'o'  as char - 97
        // 11 == 'l' as char - 97
        self.chars.iter().all(|x| match x {
            8 | 11 | 14 => false,
            _ => true,
        })
    }

    fn has_two_pairs(&self) -> bool {
        self.chars
            .windows(2)
            .filter_map(|x| match x[..] {
                [a, b] if a == b => Some(a),
                _ => None,
            })
            .collect::<HashSet<_>>()
            .len()
            >= 2
    }

    fn increment(&mut self) {
        loop {
            self.increment_unchecked();
            if self.has_chain() && self.has_no_disallowed() && self.has_two_pairs() {
                break;
            }
        }
    }
}

impl TryFrom<&str> for Password {
    type Error = anyhow::Error;

    fn try_from(value: &str) -> std::prelude::v1::Result<Self, Self::Error> {
        if value.len() != 8 {
            bail!("Password must be exactly 8 characters")
        } else {
            let mut chars = [0u8; 8];
            for (i, c) in value.chars().enumerate() {
                let value = u8::try_from(c)?;
                if value < 97 || value > 122 {
                    bail!("Non-lowercase letter '{c}'");
                } else {
                    chars[i] = (value as u8) - 97;
                }
            }
            Ok(Password { chars })
        }
    }
}

impl fmt::Display for Password {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for c in self.chars {
            write!(f, "{}", (c + 97) as char)?;
        }
        Ok(())
    }
}

fn main() -> Result<()> {
    let filename = env::args().nth(1).expect("Filename should be set");
    let pw = read_line(&filename)?;
    let mut pw = Password::try_from(pw.as_str())?;
    pw.increment();
    println!("Dec 11, part 1: {pw}");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p1() {
        let mut password1 = Password::try_from("abcdefgh").unwrap();
        password1.increment();
        let password1_next = Password::try_from("abcdffaa").unwrap();
        assert_eq!(password1, password1_next);

        let mut password2 = Password::try_from("ghijklmn").unwrap();
        password2.increment();
        let password2_next = Password::try_from("ghjaabcc").unwrap();
        assert_eq!(password2, password2_next);
    }
}
