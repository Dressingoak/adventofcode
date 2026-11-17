use anyhow::{Context, Result};
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

pub fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

pub fn read_line<P>(filename: P) -> Result<String>
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
