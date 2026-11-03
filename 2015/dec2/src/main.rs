use anyhow::{Result, bail};
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

fn iter_to_array<T, I, const N: usize>(iter: I) -> Result<[T; N]>
where
    T: Default,
    I: IntoIterator<Item = T>,
{
    let mut it = iter.into_iter();
    let mut out: [T; N] = std::array::from_fn(|_| T::default());

    let mut filled = 0;
    for (slot, item) in out.iter_mut().zip(&mut it) {
        *slot = item;
        filled += 1;
    }

    if filled < N {
        bail!("expected {N} elements, got {filled}");
    }

    let extra = it.count();
    if extra > 0 {
        bail!("expected {N} elements, got {}", N + extra);
    }

    Ok(out)
}

fn iter_result_to_array<T, I, E, const N: usize>(iter: I) -> Result<[T; N]>
where
    T: Default,
    I: IntoIterator<Item = Result<T, E>>,
    E: Into<anyhow::Error>,
{
    let mut err = None;

    let arr = iter_to_array(iter.into_iter().map_while(|item| match item {
        Ok(v) => Some(v),
        Err(e) => {
            err = Some(e);
            None
        }
    }));

    if let Some(e) = err {
        return Err(e.into());
    }
    arr
}

fn wrapping_paper(sides: [u32; 3]) -> u32 {
    let s1 = sides[0] * sides[1];
    let s2 = sides[0] * sides[2];
    let smallest = if s1 < s2 { s1 } else { s2 };
    let s3 = sides[1] * sides[2];
    let smallest = if smallest < s3 { smallest } else { s3 };
    2 * s1 + 2 * s2 + 2 * s3 + smallest
}

fn p1(data: &str) -> Result<u32> {
    let iter = data.split('x').map(|n| n.parse::<u32>());
    let sides: [u32; 3] = iter_result_to_array(iter)?;
    Ok(wrapping_paper(sides))
}

fn main() -> Result<()> {
    let filename = env::args().nth(1).expect("Filename should be set");
    let mut sum = 0;
    for line in read_lines(&filename)? {
        let wp = p1(&line?)?;
        sum += wp;
    }
    println!("Dec 1, part 1: {}", sum);
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p1() {
        assert_eq!(58, p1("2x3x4").unwrap());
        assert_eq!(43, p1("1x1x10").unwrap());
    }
}
