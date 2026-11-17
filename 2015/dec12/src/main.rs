use anyhow::Result;
use std::env;
use utils::read_line;

fn sum(json: &str) -> i32 {
    let mut sum = 0;
    let mut sign = false;
    let mut value: Option<i32> = None;
    for c in json.chars() {
        match c {
            '-' => {
                sign = true;
            }
            '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' => {
                let digit = ((c as u8) - 48) as i32;
                match &mut value {
                    Some(v) => {
                        *v *= 10;
                        *v += digit;
                    }
                    None => value = Some(digit),
                }
            }
            _ => {
                if let Some(v) = value {
                    sum += if !sign { v } else { -v };
                    sign = false;
                    value = None;
                }
            }
        }
    }
    if let Some(v) = value {
        sum += if !sign { v } else { -v };
    }
    sum
}

#[derive(Debug, Clone)]
enum JsonValue {
    Array(Vec<JsonValue>),
    Map(Vec<(String, JsonValue)>),
    Text(String),
    Number(i32),
}

enum JsonContainerType {
    Array,
    Map,
}

impl JsonValue {
    fn parse(value: &str) -> Self {
        let len = value.len();
        if let Some(c) = value.chars().next() {
            match c {
                '[' => Self::parse_inner(&value[1..(len - 1)], JsonContainerType::Array),
                '{' => Self::parse_inner(&value[1..(len - 1)], JsonContainerType::Map),
                _ => panic!("Unexpected start character: {c}"),
            }
        } else {
            panic!("Cannot handle empty string")
        }
    }

    fn parse_inner(value: &str, container: JsonContainerType) -> Self {
        let mut string_buffer = String::new();
        let mut in_string_buffer = false;
        let mut value_buffer = 0;
        let mut value_sign = false;
        let mut in_value_buffer = false;
        let mut container_buffer = String::new();
        let mut level = 0;

        let mut items = vec![];

        for c in value.chars() {
            match c {
                '[' | '{' => {
                    level += 1;
                    container_buffer.push(c);
                }
                ']' | '}' => {
                    level -= 1;
                    container_buffer.push(c);
                    if level == 0 {
                        let size = container_buffer.len();
                        let value = JsonValue::parse_inner(
                            &container_buffer[1..(size - 1)],
                            if c == ']' {
                                JsonContainerType::Array
                            } else {
                                JsonContainerType::Map
                            },
                        );
                        items.push(value);
                        container_buffer = String::new();
                    }
                }
                _ if level > 0 => {
                    container_buffer.push(c);
                }
                '\"' if !in_string_buffer => {
                    in_string_buffer = true;
                }
                '\"' if in_string_buffer => {
                    in_string_buffer = false;
                    items.push(JsonValue::Text(string_buffer.clone()));
                    string_buffer = String::new();
                }
                _ if in_string_buffer => {
                    string_buffer.push(c);
                }
                '-' => {
                    value_sign = true;
                    in_value_buffer = true;
                }
                '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' => {
                    let digit = ((c as u8) - 48) as i32;
                    value_buffer *= 10;
                    value_buffer += digit;
                    in_value_buffer = true;
                }
                ' ' => continue,
                ',' | ':' => {
                    if in_value_buffer {
                        if value_sign {
                            value_buffer *= -1
                        }
                        items.push(JsonValue::Number(value_buffer));
                        value_buffer = 0;
                        value_sign = false;
                        in_value_buffer = false;
                    }
                }
                _ => panic!("Unexpected char: {c}"),
            }
        }
        if in_value_buffer {
            if value_sign {
                value_buffer *= -1
            }
            items.push(JsonValue::Number(value_buffer));
        }
        match container {
            JsonContainerType::Array => JsonValue::Array(items),
            JsonContainerType::Map => JsonValue::Map(
                items
                    .chunks(2)
                    .map(|pair| match pair {
                        [JsonValue::Text(key), value] => (key.clone(), value.clone()),
                        _ => panic!("Expected key/value pair, got {:?}", pair),
                    })
                    .collect(),
            ),
        }
    }

    fn sum_without_reds(&self) -> i32 {
        match self {
            JsonValue::Array(items) => {
                let mut sum = 0;
                for item in items {
                    sum += item.sum_without_reds();
                }
                sum
            }
            JsonValue::Map(items) => {
                let mut sum = 0;
                for (_, value) in items {
                    match value {
                        JsonValue::Text(text) if text == "red" => return 0,
                        _ => {}
                    };
                    sum += value.sum_without_reds()
                }
                sum
            }
            JsonValue::Text(_) => 0,
            JsonValue::Number(x) => *x,
        }
    }
}

impl std::fmt::Display for JsonValue {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            JsonValue::Array(items) => {
                write!(f, "[")?;
                if let Some(item) = items.first() {
                    write!(f, "{}", item)?
                }
                for item in &items[1..] {
                    write!(f, ",{}", item)?
                }
                write!(f, "]")
            }
            JsonValue::Map(pairs) => {
                write!(f, "{{")?;
                if let Some((key, value)) = pairs.first() {
                    write!(f, "{key}:{}", value)?
                }
                for (key, value) in &pairs[1..] {
                    write!(f, ",{key}:{}", value)?
                }
                write!(f, "}}")
            }
            JsonValue::Text(text) => write!(f, "\"{text}\""),
            JsonValue::Number(number) => write!(f, "{number}"),
        }
    }
}

fn main() -> Result<()> {
    let filename = env::args().nth(1).expect("Filename should be set");
    let json = read_line(&filename)?;
    let sum = sum(&json);
    println!("Dec 12, part 1: {sum}");
    let json_parsed = JsonValue::parse(&json);
    println!("Dec 12, part 1: {}", json_parsed.sum_without_reds());
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p1() {
        assert_eq!(sum("[1,2,3]"), 6);
        assert_eq!(sum("{\"a\":2,\"b\":4}"), 6);
        assert_eq!(sum("[[[3]]]"), 3);
        assert_eq!(sum("{\"a\":{\"b\":4},\"c\":-1}"), 3);
        assert_eq!(sum("{\"a\":[-1,1]}"), 0);
        assert_eq!(sum("[-1,{\"a\":1}]"), 0);
        assert_eq!(sum("[]"), 0);
        assert_eq!(sum("{}"), 0);
    }

    #[test]
    fn test_p2() {
        let json = JsonValue::parse("{\"a\":{\"b\":4},\"c\":-1}");
        println!("JSON: {json:?}");
    }
}
