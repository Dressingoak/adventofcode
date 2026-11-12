use anyhow::{Context, Result, bail};
use std::collections::HashMap;
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

#[derive(Clone)]
enum Operand {
    Value(u16),
    Variable(String),
}

impl From<&str> for Operand {
    fn from(input: &str) -> Self {
        if let Ok(value) = input.parse::<u16>() {
            Operand::Value(value)
        } else {
            Operand::Variable(input.to_string())
        }
    }
}

#[derive(Clone)]
enum Operator {
    Assignment(Operand),
    And(Operand, Operand),
    Or(Operand, Operand),
    LShift(Operand, u16),
    RShift(Operand, u16),
    Not(Operand),
}

impl TryFrom<&str> for Operator {
    type Error = anyhow::Error;

    fn try_from(value: &str) -> std::prelude::v1::Result<Self, Self::Error> {
        let split: Vec<&str> = value.split_ascii_whitespace().collect();
        match split[..] {
            [w] => Ok(Self::Assignment(w.into())),
            [w1, "AND", w2] => Ok(Self::And(w1.into(), w2.into())),
            [w1, "OR", w2] => Ok(Self::Or(w1.into(), w2.into())),
            [w, "LSHIFT", v] => Ok(Self::LShift(w.into(), v.parse()?)),
            [w, "RSHIFT", v] => Ok(Self::RShift(w.into(), v.parse()?)),
            ["NOT", w] => Ok(Self::Not(w.into())),
            _ => bail!("Unexpected operator pattern: '{value}'"),
        }
    }
}

struct Circut {
    wires: HashMap<String, Operator>,
    resolved: HashMap<String, u16>,
}

impl Circut {
    fn configure<'a>(iter: impl Iterator<Item = &'a str>) -> Result<Self> {
        let mut wires = HashMap::new();
        for instruction in iter {
            let split: Vec<&str> = instruction.split(" -> ").collect();
            match split[..] {
                [op, w] => {
                    wires.insert(
                        w.to_string(),
                        Operator::try_from(op)
                            .with_context(|| format!("Could not parse operator '{op}'"))?,
                    );
                }
                _ => bail!("Unexpected instruction: '{instruction}'"),
            }
        }
        Ok(Circut {
            wires,
            resolved: HashMap::new(),
        })
    }

    fn emulate(&mut self, wire: &str) -> Result<u16> {
        if let Some(value) = self.resolved.get(wire) {
            Ok(*value)
        } else {
            if let Some(operator) = self.wires.get(wire).cloned() {
                let value = match operator {
                    Operator::Assignment(value) => {
                        let value = match value {
                            Operand::Value(v) => v,
                            Operand::Variable(w) => self.emulate(&w)?,
                        };
                        value
                    }
                    Operator::And(w1, w2) => {
                        let v1 = match w1 {
                            Operand::Value(v) => v,
                            Operand::Variable(w) => self.emulate(&w)?,
                        };
                        let v2 = match w2 {
                            Operand::Value(v) => v,
                            Operand::Variable(w) => self.emulate(&w)?,
                        };
                        v1 & v2
                    }
                    Operator::Or(w1, w2) => {
                        let v1 = match w1 {
                            Operand::Value(v) => v,
                            Operand::Variable(w) => self.emulate(&w)?,
                        };
                        let v2 = match w2 {
                            Operand::Value(v) => v,
                            Operand::Variable(w) => self.emulate(&w)?,
                        };
                        v1 | v2
                    }
                    Operator::LShift(w, s) => {
                        let v = match w {
                            Operand::Value(v) => v,
                            Operand::Variable(w) => self.emulate(&w)?,
                        };
                        v << s
                    }
                    Operator::RShift(w, s) => {
                        let v = match w {
                            Operand::Value(v) => v,
                            Operand::Variable(w) => self.emulate(&w)?,
                        };
                        v >> s
                    }
                    Operator::Not(w) => {
                        let v = match w {
                            Operand::Value(v) => v,
                            Operand::Variable(w) => self.emulate(&w)?,
                        };
                        !v
                    }
                };
                self.resolved.insert(wire.to_string(), value);
                Ok(value)
            } else {
                bail!("No wire named '{wire}' in circut");
            }
        }
    }
}

fn main() -> Result<()> {
    let filename = env::args().nth(1).expect("Filename should be set");
    let instructions: Result<Vec<String>, _> = read_lines(&filename)?.collect();
    let mut circut = Circut::configure(instructions?.iter().map(|s| s.as_str()))?;
    let a = circut.emulate("a")?;
    println!("Dec 7, part 1: {a}");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p1() {
        let instructions = "123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i";
        let mut circut = Circut::configure(instructions.split("\n")).unwrap();

        assert_eq!(72, circut.emulate("d").unwrap());
        assert_eq!(507, circut.emulate("e").unwrap());
        assert_eq!(492, circut.emulate("f").unwrap());
        assert_eq!(114, circut.emulate("g").unwrap());
        assert_eq!(65412, circut.emulate("h").unwrap());
        assert_eq!(65079, circut.emulate("i").unwrap());
        assert_eq!(123, circut.emulate("x").unwrap());
        assert_eq!(456, circut.emulate("y").unwrap());
    }
}
