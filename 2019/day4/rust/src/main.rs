#[macro_use] extern crate lazy_static;

fn parse_input(input: &str) -> (u32, u32) {
    use regex::Regex;

    lazy_static! {
        static ref RE: Regex = Regex::new(r"(?P<low>\d{6})-(?P<high>\d{6})").unwrap();
    }
    match RE.captures(input) {
        Some(x) => match (x.name("low"), x.name("high")) {
            (Some(low), Some(high)) => (low.as_str().parse::<u32>().unwrap(), high.as_str().parse::<u32>().unwrap()),
            _ => unreachable!(),
        }
        None => panic!("Not matched."),
    }
}

fn is_valid(number: u32) -> bool {
    if number > 99999 && number < 1000000 {
        let acceptable: Vec<bool> = number.to_string()
            .chars()
            .filter_map(|c| c.to_digit(10))
            .scan(((false, false), 0), |((dub, acceptable), prev), v| {
                if *prev > v {
                    None
                } else if *prev == v {
                    *dub = true;
                    Some(*dub)
                } else {
                    *prev = v;
                    Some(*dub)
                }
            })
            .fuse()
            .collect();
        acceptable.iter().any(|&x| x) && acceptable.len() == 6
    } else {
        false
    }
}

fn count_valid_passwords(low: u32, high: u32) -> u32 {
    (low..high)
        .map(|x| is_valid(x) as u32)
        .sum()
}

#[cfg(test)]
mod tests {
    
    #[test]
    fn test_parsing() {
        use super::parse_input;

        let (low, high) = parse_input("123456-987654");
        assert_eq!(low, 123456);
        assert_eq!(high, 987654);
    }

    #[test]
    fn test_is_valid() {
        use super::is_valid;

        assert_eq!(is_valid(111111), true);
        assert_eq!(is_valid(223450), false);
        assert_eq!(is_valid(123789), false);
    }
}

fn main() {
    let (low, high) = parse_input("264793-803935");
    let count = count_valid_passwords(low, high);
    println!("Part 1: {}", count);
}
