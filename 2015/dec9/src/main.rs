use anyhow::{Context, Result, bail};
use std::collections::{HashMap, HashSet};
use std::collections::hash_map::Entry;
use std::env;
use std::fs::File;
use std::hash::Hash;
use std::io::{self, BufRead};
use std::iter::once;
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
    edges: HashMap<(usize, usize), u32>
}

impl<T> UndirectedGraph<T>
where T: Eq + Hash,
(T, T): Eq + Hash {
    fn add(&mut self, node: Node<T>) -> Result<()> {
        let Node { from, to, weight } = node;
        let from_index = self.nodes.iter().position(|x| x == &from);
        let to_index = self.nodes.iter().position(|x| x == &to);
        let (i, j) = match (from_index, to_index) {
            (Some(i), Some(j)) => {
                (i, j)
            }
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

    // fn travelling_salesman(&self) -> u32 {

    // }

    fn _node_permutations<'a>(&'a self, used: Vec<usize>, current: Vec<&str>) -> impl Iterator<Item = Vec<&'a T>> {
        todo!()
    }
}

struct Permutations<'a, T> {
    k: usize,
    arr: Vec<&'a T>,
}

struct InnerPermutations<'a, T> {
    inner: Vec<>
}

impl<'a, T> Iterator for Permutations<'a, T> {
    type Item = Vec<&'a T>;

    fn next(&mut self) -> Option<Self::Item> {
        match self.k {
            0 => None,
            1 => {
                self.k = 0;
                Some(self.arr)
            },
            k => {
                let mut iters = Vec::with_capacity(k+1);
                iters.push(Permutations {
                    k: k -1,
                    arr: self.arr.clone(),
                });
                for i in 0..(k-1) {
                    let arr = self.arr.clone();
                    if k % 2 == 0 {
                        arr.swap(i, k-1);
                    } else {
                        arr.swap(0, k-1);
                    }
                    iters.push(Permutations { k: k - 1, arr });
                }
                iters.iter().flat_map(|iter| iter)
            }
        }
    }
}

fn permutations<'a, T>(k: usize, mut arr: Vec<&'a T>) -> impl Iterator<Item = Vec<&'a T>> {
    if k == 1 {
        once(arr)
    } else {
        let mut iters: Vec<impl > = Vec::with_capacity(k+1);
        iters.push(permutations(k - 1, arr));
        for i in 0..(k-1) {
            if k % 2 == 0 {
                arr.swap(i, k-1);
            } else {
                arr.swap(0, k-1);
            }
            iters.push(permutations(k - 1, arr));
        }
        iters.iter().flat_map(|iter| iter)
    }
}

fn parse(line: &str) -> Result<Node<String>> {
    let split: Vec<_> = line.split_ascii_whitespace().collect();
    match split[..] {
        [a, "to", b, "=", distance] => {
            let weight = distance.parse()?;
            Ok(Node { from: a.to_string(), to: b.to_string(), weight })
        },
        _ => bail!("Unexpected pattern: '{line}'")
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
    let a = circut.emulate("a")?;
    println!("Dec 7, part 1: {a}");
    Ok(())
}

// #[cfg(test)]
// mod tests {
//     use super::*;

//     #[test]
//     fn test_p1() {
//         let instructions = "London to Dublin = 464
// London to Belfast = 518
// Dublin to Belfast = 141";
//         let mut circut = Circut::configure(instructions.split("\n")).unwrap();

//         assert_eq!(72, circut.emulate("d").unwrap());
//         assert_eq!(507, circut.emulate("e").unwrap());
//         assert_eq!(492, circut.emulate("f").unwrap());
//         assert_eq!(114, circut.emulate("g").unwrap());
//         assert_eq!(65412, circut.emulate("h").unwrap());
//         assert_eq!(65079, circut.emulate("i").unwrap());
//         assert_eq!(123, circut.emulate("x").unwrap());
//         assert_eq!(456, circut.emulate("y").unwrap());
//     }
// }
