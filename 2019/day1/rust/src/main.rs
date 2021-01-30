fn required_fuel(x: u32) -> u32 {
    x / 3 - 2
}

#[cfg(test)]
mod tests {
    use super::required_fuel;

    #[test]
    fn test_a() { assert_eq!(required_fuel(12), 2); }

    #[test]
    fn test_b() { assert_eq!(required_fuel(14), 2); }

    #[test]
    fn test_c() { assert_eq!(required_fuel(1969), 654); }

    #[test]
    fn test_d() { assert_eq!(required_fuel(100756), 33583); }
}

fn main() {
    use std::fs;

    let filename = "input.txt";
    let fuel_requirements: u32 = fs::read_to_string(filename)
        .expect("Something went wrong reading the file")
        .lines()
        .map(|x| {
            let weight: u32 = x.parse().unwrap();
            required_fuel(weight)
        })
        .fold(0, |a, b| a + b);

    println!("Par1 1: {}", fuel_requirements);
}
