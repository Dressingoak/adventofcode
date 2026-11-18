use anyhow::{Result, bail};
use std::env;
use utils::read_lines;

struct Reindeer {
    speed: u32,
    duration: u32,
    rest: u32,
}

impl Reindeer {
    fn position_after(&self, seconds: u32) -> u32 {
        let period = self.duration + self.rest;
        let (q, r) = (seconds / period, seconds % period);
        self.speed * (q * self.duration + r.min(self.duration))
    }
}

fn parse(input: &str) -> Result<Reindeer> {
    let split: Vec<&str> = input.split_ascii_whitespace().collect();
    Ok(match split[..] {
        [
            _, // name
            "can",
            "fly",
            speed,
            "km/s",
            "for",
            duration,
            "seconds,",
            "but",
            "then",
            "must",
            "rest",
            "for",
            rest,
            "seconds.",
        ] => Reindeer {
            speed: speed.parse()?,
            duration: duration.parse()?,
            rest: rest.parse()?,
        },
        _ => bail!("Unrecognized pattern: {input}"),
    })
}

fn main() -> Result<()> {
    let filename = env::args().nth(1).expect("Filename should be set");
    let mut max: Option<u32> = None;
    for line in read_lines(&filename)? {
        let line = line?;
        let reindeer = parse(&line)?;
        let position = reindeer.position_after(2503);
        max = match max {
            Some(m) => Some(m.max(position)),
            None => Some(position),
        }
    }
    println!("Dec 14, part 1: {}", max.unwrap());
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p1() -> Result<()> {
        let comet = Reindeer {
            speed: 14,
            duration: 10,
            rest: 127,
        };
        assert_eq!(comet.position_after(1000), 1120);

        let dancer = Reindeer {
            speed: 16,
            duration: 11,
            rest: 162,
        };
        assert_eq!(dancer.position_after(1000), 1056);
        Ok(())
    }
}
