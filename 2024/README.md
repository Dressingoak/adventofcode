# Advent of Code 2024
All solutions use Python (tested with 3.12).

## Individual execution
To run,
* `cd` into the desired folder (e.g. `cd dec1/`)
* run `python test.py` to verify the algorithm on the test input
* run `python solution.py` to execute the script on the actual input

## CLI tool
Run
```shell
python main.py -h
```
for a guide on how to use. Quick start:
```shell
python main.py run # Run all solutions
python main.py -d 1 -p 2 run # Run solution for Dec 1 part 2
python main.py -d 2 run # Run solution for Dec 2 (part 1 and 2)
python main.py -f "test.txt" run # Run all solutions with test input
python main.py -d 1 -p 2 --no-local -f "dec1/test2.txt" run # Run Dec 1 part 2 using the "dec1/test2.txt" file in the actual filesystem (usable when running the Docker container version described below with a mounted folder)
python main.py timeit # Time all solutions with default number of executions and repetitions
python main.py -d 4 -p 1 timeit -r 100 -n 10 # Time Dec 4 part 1 with 100 repetitions of 10 executions
```

## Docker
Docker wrapper for the CLI tool. Usage is the same as above. Build with:
```shell
docker build . -t aoc-2024
```

Get help section of the CLI:
```shell
docker run -t aoc-2024 -h
```
