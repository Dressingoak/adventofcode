import argparse
import glob
import importlib.util
import timeit
import time
import math

choices = sorted([int(f.rstrip("/\\")[3:]) for f in glob.glob("dec*/")])
with open("art.txt") as f:
    ascii_art = f.read()

# create the top-level parser
parser = argparse.ArgumentParser(
    prog="aoc-2023",
    description=f"{ascii_art}\nAdvent of Code 2023 solutions",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

subparsers = parser.add_subparsers(help="command to run on selected days and parts")
parser.add_argument(
    "-d",
    "--day",
    type=int,
    required=False,
    choices=choices,
    metavar="D",
    help="specific day to pick",
)

parser.add_argument(
    "-p",
    "--part",
    type=int,
    required=False,
    choices=[1, 2],
    metavar="P",
    help="specific part to pick",
)

parser.add_argument(
    "-f",
    "--file",
    required=False,
    default="input.txt",
    metavar="F",
    help="file to use",
)

parser.add_argument(
    "-l",
    "--local",
    required=False,
    default=True,
    action=argparse.BooleanOptionalAction,
    help="use local file structure (i.e. 'test.txt' will point to the file in the day folder)",
)

parser_run = subparsers.add_parser("run", help="run solutions")
parser_run.set_defaults(which="run")
parser_timeit = subparsers.add_parser("timeit", help="time solution (with timeit)")
parser_timeit.set_defaults(which="timeit")
parser_timeit.add_argument(
    "-n",
    "--number",
    type=int,
    metavar="N",
    required=False,
    default=1,
    help="number of executions",
)
parser_timeit.add_argument(
    "-r",
    "--repeats",
    type=int,
    metavar="R",
    required=False,
    default=10,
    help="number of repeats of the specified number of executions",
)

args = parser.parse_args()
if not hasattr(args, "which"):
    print(parser.format_help())
    parser.exit()

days = [args.day] if args.day is not None else choices
parts = [args.part] if args.part is not None else [1, 2]


paths = f"dec<day>/{args.file}"
print(f"Running {days=}, {parts=}, {paths=}, {args.which=}")
if args.which == "timeit":
    print(
        f"Repeats: {args.repeats}, number of executions within each repetition: {args.number}"
    )


for day in days:
    print("---")
    spec = importlib.util.spec_from_file_location("solution", f"dec{day}/solution.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(args, "local") and args.local is True:
        path = f"dec{day}/{args.file}"
    else:
        path = args.file
    for part in parts:
        match part:
            case 1:
                fun = module.part1
            case 2:
                fun = module.part2
        day_str = f"Dec {day}, part {part}: "
        match args.which:
            case "run":
                start = time.perf_counter()
                v = fun(path)
                duration = (time.perf_counter() - start) * 1_000
                if duration < 10:
                    duration_formatted = f"{duration:.1f}"
                else:
                    duration_formatted = f"{duration:.0f}"
                print(f"{day_str}{v} ({duration_formatted} ms)")
            case "timeit":
                with open(f"dec{day}/solution.py") as f:
                    stmt = f"part{part}('{path}')"
                    t = timeit.Timer(stmt=stmt, setup=f.read())
                    duration = (
                        min(t.repeat(repeat=args.repeats, number=args.number))
                        / args.number
                        * 1000
                    )
                    timing = f"{day_str}{duration:.3f} ms"
                    w = duration // 10
                    
                    print(f"{timing: <30}| {' ':-<{w}}o")
