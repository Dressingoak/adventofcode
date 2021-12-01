fn transform_data(data: String) -> Vec<u32> {
    data
        .split_whitespace()
        .map(|x| x.parse::<u32>().unwrap())
        .collect()
}

fn count_increases(measurements: Vec<u32>) -> usize {
    measurements
        .iter()
        .scan(None::<u32>, |prev_opt, &cur| {
            let increases = match *prev_opt {
                Some(prev) if cur > prev => 1,
                _ => 0,
            };
            *prev_opt = Some(cur);
            Some(increases)
        })
        .sum()
}

fn calculate(input: String) -> usize {
    count_increases(transform_data(input))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calculate() {
        let data = include_str!("../test.txt").to_string();
        assert_eq!(7, calculate(data));
    }
}

fn main() {
    let data = include_str!("../input.txt").to_string();
    println!("Dec 1, part 1: {}", calculate(data));
}
