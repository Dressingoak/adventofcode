use anyhow::{Result, bail};
use std::collections::HashMap;
use std::env;
use std::fmt::Display;
use std::fs::File;
use std::hash::Hash;
use std::io::{self, BufRead};
use std::path::Path;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

struct Node<T> {
    from: T,
    to: T,
    weight: u32,
}

#[derive(Default)]
struct UndirectedGraph<T> {
    nodes: Vec<T>,
    edges: HashMap<(usize, usize), u32>,
}

impl<T> UndirectedGraph<T>
where
    T: Eq + Hash,
{
    fn add(&mut self, node: Node<T>) -> Result<()> {
        let Node { from, to, weight } = node;
        let from_index = self.nodes.iter().position(|x| x == &from);
        let to_index = self.nodes.iter().position(|x| x == &to);
        let (i, j) = match (from_index, to_index) {
            (Some(i), Some(j)) => (i, j),
            (Some(i), None) => {
                self.nodes.push(to);
                let j = self.nodes.len() - 1;
                (i, j)
            }
            (None, Some(j)) => {
                self.nodes.push(from);
                let i = self.nodes.len() - 1;
                (i, j)
            }
            (None, None) => {
                self.nodes.push(from);
                self.nodes.push(to);
                let i = self.nodes.len() - 2;
                let j = self.nodes.len() - 1;
                (i, j)
            }
        };
        self.edges.insert((i, j), weight);
        self.edges.insert((j, i), weight);
        Ok(())
    }

    fn get(&self, a: &T, b: &T) -> Option<u32> {
        let from_index = self.nodes.iter().position(|x| x == a)?;
        let to_index = self.nodes.iter().position(|x| x == b)?;
        self.edges.get(&(from_index, to_index)).cloned()
    }

    fn travelling_salesman(&self) -> u32
    where
        T: Display,
    {
        let refs: Vec<&T> = self.nodes.iter().collect();
        let n = refs.len();
        permutations(refs)
            .chunks(n)
            .map(|nodes| {
                let mut cost = 0;
                for wd in nodes.windows(2) {
                    match wd {
                        &[a, b] => {
                            if let Some(w) = self.get(a, b) {
                                cost += w;
                            } else {
                                panic!("Could not find weight");
                            }
                        }
                        _ => unreachable!(),
                    }
                }
                cost
            })
            .fold(None, |acc, cost| match acc {
                None => Some(cost),
                Some(prev) => Some(prev.min(cost)),
            })
            .unwrap()
    }
}

fn fact(n: usize) -> usize {
    match n {
        0 => 1,
        1 => 1,
        n => n * fact(n - 1),
    }
}

fn permutations<T>(mut arr: Vec<&T>) -> Vec<&T> {
    let n = arr.len();
    let mut res = Vec::with_capacity(fact(n) * arr.len());
    let mut c = vec![0; n];
    res.extend(arr.iter());

    let mut i = 1;
    while i < n {
        if c[i] < i {
            if i % 2 == 0 {
                arr.swap(0, i);
            } else {
                arr.swap(c[i], i);
            }
            res.extend(arr.iter());
            c[i] += 1;
            i = 1;
        } else {
            c[i] = 0;
            i += 1;
        }
    }

    res
}

fn parse(line: &str) -> Result<Node<String>> {
    let split: Vec<_> = line.split_ascii_whitespace().collect();
    match split[..] {
        [a, "to", b, "=", distance] => {
            let weight = distance.parse()?;
            Ok(Node {
                from: a.to_string(),
                to: b.to_string(),
                weight,
            })
        }
        _ => bail!("Unexpected pattern: '{line}'"),
    }
}

fn main() -> Result<()> {
    let filename = env::args().nth(1).expect("Filename should be set");
    let mut graph = UndirectedGraph::default();
    for l in read_lines(&filename)? {
        let line = l?;
        let node = parse(&line)?;
        graph.add(node)?;
    }
    let res = graph.travelling_salesman();
    println!("Dec 9, part 1: {res}");
    Ok(())
}

#[cfg(test)]
mod tests {
    use std::collections::HashSet;

    use super::*;

    #[test]
    fn test_permutations() {
        const N: usize = 3;
        let vals = Vec::from_fn(N, |i| char::from_u32((i + 65) as u32).unwrap());
        let arr = permutations(vals.iter().collect());
        let mut set = HashSet::new();
        for chunk in arr.chunks(N) {
            let arr: [char; N] = chunk
                .iter()
                .map(|&x| *x)
                .collect::<Vec<_>>()
                .try_into()
                .unwrap();
            set.insert(arr);
            println!("{chunk:?}");
        }
        assert!(set.contains(&['A', 'B', 'C']));
        assert!(set.contains(&['B', 'A', 'C']));
        assert!(set.contains(&['A', 'C', 'B']));
        assert!(set.contains(&['C', 'A', 'B']));
        assert!(set.contains(&['B', 'C', 'A']));
        assert!(set.contains(&['C', 'B', 'A']));
    }
}
