fn required_fuel(x: u32) -> u32 {
    let calc = (x / 3).checked_sub(2);
    match calc {
        Some(res) => res,
        None => 0
    }
}

fn required_fuel_including_own_weight(x: u32) -> u32 {
    let mut total = 0u32;
    let mut current = x;
    loop {
        let additional = required_fuel(current);
        if additional == 0 {
            break total;
        } else {
            total += additional;
            current = additional;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_required_fuel() { 
        assert_eq!(required_fuel(12), 2); 
        assert_eq!(required_fuel(14), 2);
        assert_eq!(required_fuel(1969), 654);
        assert_eq!(required_fuel(100756), 33583);
    }

    #[test]
    fn test_required_fuel_including_own_weight() {
        assert_eq!(required_fuel_including_own_weight(14), 2); 
        assert_eq!(required_fuel_including_own_weight(1969), 654 + 216 + 70 + 21 + 5);
        assert_eq!(required_fuel_including_own_weight(100756), 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2); 
    }
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

    let total_fuel_requirements: u32 = fs::read_to_string(filename)
        .expect("Something went wrong reading the file")
        .lines()
        .map(|x| {
            let weight: u32 = x.parse().unwrap();
            required_fuel_including_own_weight(weight)
        })
        .fold(0, |a, b| a + b);

    println!("Par1 2: {}", total_fuel_requirements);
}
