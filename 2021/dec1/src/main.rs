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

fn sum_sliding_windows(measurements: Vec<u32>) -> Vec<u32> {
    measurements
        .iter()
        .as_slice()
        .windows(3)
        .map(|s| s.iter().sum())
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p1() {
        let data = include_str!("../test.txt").to_string();
        let measurements = transform_data(data);
        assert_eq!(7, count_increases(measurements));
    }

    #[test]
    fn test_p2() {
        let data = include_str!("../test.txt").to_string();
        let measurements = transform_data(data);
        let sw_measurements = sum_sliding_windows(measurements);
        assert_eq!(5, count_increases(sw_measurements));
    }
}

fn main() {
    let data = include_str!("../input.txt").to_string();
    let measurements = transform_data(data);
    println!("Dec 1, part 1: {}", count_increases(measurements.clone()));

    let sw_measurements = sum_sliding_windows(measurements);
    println!("Dec 1, part 2: {}", count_increases(sw_measurements));
}
