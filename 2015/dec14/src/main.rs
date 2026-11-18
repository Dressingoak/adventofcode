use anyhow::{Result, bail};
use std::{collections::HashMap, env};
use utils::read_lines;

struct Reindeer {
    name: String,
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
            name,
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
            name: name.to_string(),
            speed: speed.parse()?,
            duration: duration.parse()?,
            rest: rest.parse()?,
        },
        _ => bail!("Unrecognized pattern: {input}"),
    })
}

fn max_score(reindeers: Vec<Reindeer>, after: u32) -> u32 {
    let mut scores = HashMap::new();
    for seconds in 1..=after {
        let positions: HashMap<_, _> = reindeers
            .iter()
            .map(|reindeer| (reindeer.name.clone(), reindeer.position_after(seconds)))
            .collect();
        let lead_position = *positions.values().max().unwrap();
        positions
            .into_iter()
            .filter_map(|(name, position)| {
                if position == lead_position {
                    Some(name)
                } else {
                    None
                }
            })
            .for_each(|name| {
                scores.entry(name).and_modify(|e| *e += 1).or_insert(1);
            });
    }
    // println!("Scores: {:?}", scores);
    *scores.values().max().unwrap()
}

fn main() -> Result<()> {
    let time_limit = 2503;
    let filename = env::args().nth(1).expect("Filename should be set");
    let mut max: Option<u32> = None;
    let mut reindeers = vec![];
    for line in read_lines(&filename)? {
        let line = line?;
        let reindeer = parse(&line)?;
        let position = reindeer.position_after(time_limit);
        max = match max {
            Some(m) => Some(m.max(position)),
            None => Some(position),
        };
        reindeers.push(reindeer);
    }
    println!("Dec 14, part 1: {}", max.unwrap());
    let score = max_score(reindeers, time_limit);
    println!("Dec 14, part 2: {}", score);
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p1() {
        let comet = Reindeer {
            name: "Comet".to_string(),
            speed: 14,
            duration: 10,
            rest: 127,
        };
        assert_eq!(comet.position_after(1000), 1120);

        let dancer = Reindeer {
            name: "Dancer".to_string(),
            speed: 16,
            duration: 11,
            rest: 162,
        };
        assert_eq!(dancer.position_after(1000), 1056);
    }

    #[test]
    fn test_p2() {
        let reindeers = vec![
            Reindeer {
                name: "Comet".to_string(),
                speed: 14,
                duration: 10,
                rest: 127,
            },
            Reindeer {
                name: "Dancer".to_string(),
                speed: 16,
                duration: 11,
                rest: 162,
            },
        ];
        assert_eq!(max_score(reindeers, 1000), 689);
    }
}
