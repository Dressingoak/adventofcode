#[macro_use] extern crate lazy_static;
use std::fmt;
use std::collections::HashSet;

#[derive(Copy, Clone, Hash, PartialEq, Eq, Debug)]
struct Point {
    x: i32,
    y: i32
}

impl Point {
    fn origin() -> Point {
        Point { x: 0, y: 0 }
    }

    fn dist(&self, other: &Point) -> u32 {
        ((self.x - other.x).abs() + (self.y - other.y).abs()) as u32
    }

    fn add(&self, dir: Direction, len: u32) -> Point {
        match dir {
            Direction::Left  => Point { x: self.x - len as i32, y: self.y},
            Direction::Down  => Point { x: self.x, y: self.y - len as i32},
            Direction::Right => Point { x: self.x + len as i32, y: self.y},
            Direction::Up    => Point { x: self.x, y: self.y + len as i32}
        }
    }
}

impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

#[derive(Copy, Clone, PartialEq, Eq, Debug)]
enum Direction {
    Left,
    Down,
    Right,
    Up
}

impl Direction {
    fn create(direction: char) -> Direction {
        match direction {
            'L' => Direction::Left,
            'D' => Direction::Down,
            'R' => Direction::Right,
            'U' => Direction::Up,
            _ => panic!("Unrecognized character.")
        }
    }
}


impl fmt::Display for Direction {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Direction::Left => write!(f, "left"),
            Direction::Down => write!(f, "down"),
            Direction::Right => write!(f, "right"),
            Direction::Up => write!(f, "up")
        }
        
    }
}

trait Orientation {
    fn is_horizontal(&self) -> bool;
    fn is_vetical(&self) -> bool;
    fn is_same(&self, other: &dyn Orientation) -> bool;
}

impl Orientation for Direction {
    fn is_horizontal(&self) -> bool {
        match self {
            Direction::Left => true,
            Direction::Right => true,
            _ => false
        }
    }

    fn is_vetical(&self) -> bool {
        match self {
            Direction::Up => true,
            Direction::Down => true,
            _ => false
        }
    }

    fn is_same(&self, other: &dyn Orientation) -> bool {
        self.is_horizontal() && other.is_horizontal() || self.is_vetical() && other.is_vetical()
    }
}

#[derive(PartialEq, Eq, Debug)]
struct LineSegment {
    start: Point,
    direction: Direction,
    length: u32
}

impl LineSegment {

    pub fn end(&self) -> Point {
        self.start.add(self.direction, self.length)
    }

    pub fn get_points(&self) -> (Point, Point) {
        match self.direction {
            Direction::Left  => (self.end(), self.start),
            Direction::Down  => (self.end(), self.start),
            Direction::Right => (self.start, self.end()),
            Direction::Up    => (self.start, self.end())
        }
    }

    pub fn cross(&self, other: &LineSegment) -> Option<Point>{
        let points: Option<(Point, Point, Point, Point)> = if self.direction.is_vetical() {
            if other.direction.is_vetical() {
                None
            } else {
                let (left, right) = other.get_points();
                let (down, up) = self.get_points();
                Some((left, right, down, up))
            }
        } else {
            if other.direction.is_horizontal() {
                None
            } else {
                let (left, right) = self.get_points();
                let (down, up) = other.get_points();
                Some((left, right, down, up))
            }
        };
        match points {
            Some((left, right, down, up)) => {
                if left.x <= down.x && down.x <= right.x && down.y <= left.y && left.y <= up.y {
                    Some(Point{ x: down.x, y: left.y })
                } else {
                    None
                }
            }
            None => {
                None
            }
        }
    }

    fn get_segments(instructions: &String) -> Vec<LineSegment> {
        use regex::Regex;

        lazy_static! {
            static ref RE: Regex = Regex::new(r"((?P<direction>L|D|R|U)(?P<length>\d+))").unwrap();
        }

        RE.captures_iter(instructions)
            .scan(Point::origin(), |state, x: regex::Captures| {
                let direction = Direction::create(x["direction"].chars().next().unwrap());
                let length = x["length"].parse::<u32>().unwrap();
                let ls = LineSegment {
                    start: state.clone(),
                    direction,
                    length
                };
                *state = state.add(direction, length);
                Some(ls)
            })
            .collect()
    }

    fn intersections(left: &Vec<LineSegment>, right: &Vec<LineSegment>) -> HashSet<Point> {
        use itertools::Itertools;

        left.iter()
            .cartesian_product(right.iter())
            .filter_map(|(l, r)| l.cross(r))
            .filter(|p| *p != Point::origin())
            .collect()
    }
}

impl fmt::Display for LineSegment {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({}, {}, {})", self.start, self.direction, self.length)
    }
}

fn minimal_distance_to_intersections(filename: &str) -> Option<u32> {
    use std::fs;

    let wires: Vec<Vec<LineSegment>> = fs::read_to_string(filename)
        .expect("Something went wrong reading the file.")
        .lines()
        .map(|ins| LineSegment::get_segments(&ins.to_string()))
        .collect();
    if wires.len() != 2 { 
        panic!("Expected 2 wires in file '{}', but got {}", filename, wires.len()) 
    }
    LineSegment::intersections(&wires[0], &wires[1]).iter()
        .map(|p| p.dist(&Point::origin()))
        .min()
}

#[cfg(test)]
mod tests {
    use super::Point;
    use super::Direction;
    use super::LineSegment;
    
    #[test]
    fn test_construction() {
        let segment = LineSegment{ start: Point { x: 1, y: 7}, direction: Direction::Left, length: 4};
        let (a, b) = segment.get_points();
        assert_eq!(a, Point { x: -3, y: 7});
        assert_eq!(b, Point { x: 1, y: 7});
    }

    #[test]
    fn test_parsing() {
        let data = "R8,U5,L5,D3".to_string();
        let segments = LineSegment::get_segments(&data);
        assert_eq!(segments.len(), 4);
        assert_eq!(segments[0], LineSegment{ start: Point { x: 0, y: 0}, direction: Direction::Right, length: 8 } );
        assert_eq!(segments[1], LineSegment{ start: Point { x: 8, y: 0}, direction: Direction::Up,    length: 5 } );
        assert_eq!(segments[2], LineSegment{ start: Point { x: 8, y: 5}, direction: Direction::Left,  length: 5 } );
        assert_eq!(segments[3], LineSegment{ start: Point { x: 3, y: 5}, direction: Direction::Down,  length: 3 } );
    }

    #[test]
    fn test_cross() {
        {
            let a = LineSegment{ start: Point { x: -2, y: 0}, direction: Direction::Right, length: 4};
            let b = LineSegment{ start: Point { x: 0, y: -2}, direction: Direction::Up, length: 4};
            assert_eq!(a.cross(&b), Some(Point::origin()));
        }
        {
            let a = LineSegment{ start: Point { x: -2, y: 0}, direction: Direction::Down, length: 4};
            let b = LineSegment{ start: Point { x: 0, y: -2}, direction: Direction::Up, length: 4};
            assert_eq!(a.cross(&b), None);
        }
        {
            let a = LineSegment{ start: Point { x: 0, y: 0}, direction: Direction::Right, length: 4};
            let b = LineSegment{ start: Point { x: 3, y: 1}, direction: Direction::Down, length: 2};
            assert_eq!(a.cross(&b), Some(Point { x: 3, y: 0 }));
        }
        {
            let a = LineSegment{ start: Point { x: 0, y: 0}, direction: Direction::Right, length: 4};
            let b = LineSegment{ start: Point { x: 5, y: 1}, direction: Direction::Down, length: 2};
            assert_eq!(a.cross(&b), None);
        }
    }

    #[test]
    fn test_multiple_crosses() {
        use std::collections::HashSet;

        let segments_a = LineSegment::get_segments(&String::from("R8,U5,L5,D3"));
        let segments_b = LineSegment::get_segments(&String::from("U7,R6,D4,L4"));
        let crosses = LineSegment::intersections(&segments_a, &segments_b);
        let expected: HashSet<Point> = [Point{ x: 3, y: 3}, Point{ x: 6, y: 5}].iter().cloned().collect();
        assert_eq!(crosses.len(), 2);
        assert_eq!(crosses, expected);
        let dist = crosses.iter()
            .map(|p| p.dist(&Point::origin()))
            .min();
        assert_eq!(dist, Some(6));
    }

    #[test]
    fn test_examples() {
        {
            let dist = super::minimal_distance_to_intersections("test1.txt");
            assert_eq!(dist, Some(159))
        }
        {
            let dist = super::minimal_distance_to_intersections("test2.txt");
            assert_eq!(dist, Some(135))
        }
    }
}

fn main() {
    let dist = minimal_distance_to_intersections("input.txt");
    match dist {
        Some(value) => println!("Part 1: {}", value),
        None => panic!("Part 1: Failed to find any intersections.")
    }
}
