struct Intcode {
    values: Vec<u32>
}

impl Intcode {
    fn create(instructions: String) -> Intcode {
        let values: Vec<u32> = instructions.split(",").map(|x| x.parse::<u32>().unwrap()).collect();
        Intcode { values }
    }

    fn update(&mut self, pos: usize, value: u32) -> u32 {
        std::mem::replace(&mut self.values[pos], value)
    }

    pub fn run(&mut self) -> u32 {
        let mut pos: usize = 0;
        loop {
            if self.values[pos] == 99 {
                break self.values[0];
            } else {
                let lhs = self.values[pos + 1] as usize;
                let rhs = self.values[pos + 2] as usize;
                let idx = self.values[pos + 3] as usize;
                if self.values[pos] == 1 {
                    self.update(idx, self.values[lhs] + self.values[rhs]);
                } else if self.values[pos] == 2 {
                    self.update(idx, self.values[lhs] * self.values[rhs]);
                }
                pos += 4;
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::Intcode;

    #[test]
    fn test_construction() {
        let code = Intcode::create(String::from("1,0,0,0,99"));
        assert_eq!(code.values, vec![1,0,0,0,99]); 
    }

    #[test]
    fn test_updating() {
        let mut code = Intcode::create(String::from("1,0,0,0,99"));
        code.update(1, 12);
        assert_eq!(code.values[1], 12); 
    }

    #[test]
    fn test_run_ex1() {
        let mut code = Intcode::create(String::from("1,0,0,0,99"));
        code.run();
        assert_eq!(code.values, vec![2,0,0,0,99]); 
    }

    #[test]
    fn test_run_ex2() {
        let mut code = Intcode::create(String::from("2,3,0,3,99"));
        code.run();
        assert_eq!(code.values, vec![2,3,0,6,99]); 
    }

    #[test]
    fn test_run_ex3() {
        let mut code = Intcode::create(String::from("2,4,4,5,99,0"));
        code.run();
        assert_eq!(code.values, vec![2,4,4,5,99,9801]); 
    }

    #[test]
    fn test_run_ex4() {
        let mut code = Intcode::create(String::from("1,1,1,4,99,5,6,0,99"));
        code.run();
        assert_eq!(code.values, vec![30,1,1,4,2,5,6,0,99]); 
    }
}

fn main() {
    use std::fs;

    let filename = "input.txt";
    let instructions: String = fs::read_to_string(filename)
        .expect("Something went wrong reading the file")
        .chars()
        .filter(|c| !c.is_whitespace())
        .collect();
    let mut code = Intcode::create(instructions);
    code.update(1, 12);
    code.update(2, 2);
    let res = code.run();
    println!("Part 1: {}", res);
}
