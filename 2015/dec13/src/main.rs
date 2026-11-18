use anyhow::{Result, bail};
use std::hash::Hash;
use std::{collections::HashMap, env, fmt::Display, iter::once};
use utils::read_lines_to_vec;

struct Node<T> {
    from: T,
    to: T,
    weight: i32,
}

#[derive(Debug, Default)]
struct DirectedGraph<T> {
    nodes: Vec<T>,
    edges: HashMap<(usize, usize), i32>,
}

impl<T> DirectedGraph<T>
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
        Ok(())
    }

    fn get(&self, a: &T, b: &T) -> Option<i32> {
        let from_index = self.nodes.iter().position(|x| x == a)?;
        let to_index = self.nodes.iter().position(|x| x == b)?;
        self.edges.get(&(from_index, to_index)).cloned()
    }

    fn travelling_salesman_wrap(&self) -> (i32, i32)
    where
        T: Display,
    {
        let refs: Vec<&T> = self.nodes.iter().collect();
        let n = refs.len();
        permutations(refs)
            .chunks(n)
            .map(|nodes| {
                let nodes: Vec<_> = nodes.iter().chain(once(nodes.first().unwrap())).collect();
                let mut cost = 0;
                for wd in nodes.windows(2) {
                    match wd {
                        &[a, b] => {
                            if let Some(w) = self.get(a, b) {
                                cost += w;
                            } else {
                                panic!("Could not find weight");
                            }
                            if let Some(w) = self.get(b, a) {
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
                None => Some((cost, cost)),
                Some((prev_min, prev_max)) => Some((prev_min.min(cost), prev_max.max(cost))),
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

fn main() -> Result<()> {
    let filename = env::args().nth(1).expect("Filename should be set");
    let lines = read_lines_to_vec(&filename)?;
    let graph = parse(lines.iter())?;
    let (_, max_happiness) = graph.travelling_salesman_wrap();
    println!("Dec 13, part 1: {max_happiness}");
    Ok(())
}

fn parse<'a, I>(iter: I) -> Result<DirectedGraph<String>>
where
    I: IntoIterator,
    I::Item: AsRef<str>,
{
    let mut graph = DirectedGraph::default();
    for line in iter {
        let split: Vec<&str> = line.as_ref().split_ascii_whitespace().collect();
        let node = match split[..] {
            [
                a,
                "would",
                "gain",
                x,
                "happiness",
                "units",
                "by",
                "sitting",
                "next",
                "to",
                b,
            ] => Node {
                from: a.to_string(),
                to: b[..b.len() - 1].to_string(),
                weight: x.parse()?,
            },
            [
                a,
                "would",
                "lose",
                x,
                "happiness",
                "units",
                "by",
                "sitting",
                "next",
                "to",
                b,
            ] => Node {
                from: a.to_string(),
                to: b[..b.len() - 1].to_string(),
                weight: -x.parse()?,
            },
            _ => bail!("Unrecognized pattern: {}", line.as_ref()),
        };
        graph.add(node)?;
    }
    Ok(graph)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p1() -> Result<()> {
        let lines = read_lines_to_vec("test.txt")?;
        let graph = parse(lines.iter())?;
        let (_, max_happiness) = graph.travelling_salesman_wrap();
        assert_eq!(max_happiness, 330);
        Ok(())
    }
}
