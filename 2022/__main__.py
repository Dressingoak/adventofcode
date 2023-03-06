import argparse
import importlib
import sys
from puzzle import Puzzle

modules = {day: importlib.import_module(f"dec{day}.solution") for day in range(1, 26)}

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
Puzzle.add_general_group(parser)

subparsers = parser.add_subparsers()
all_func = []

for day, module in modules.items():
    subparser = subparsers.add_parser(f"dec{day}", help=f'run solution(s) for Dec {day} {module.puzzle.year}', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    module.puzzle.build_parser(subparser)
    subparser.set_defaults(func=module.puzzle.run)
    all_func.append(module.puzzle)

def run_all_func(args: argparse.Namespace):
    outer_args = {k: v for k, v in args.__dict__.items() if k != "func"}
    for puzzle in all_func:
        inner_args: argparse.Namespace = {k: v for k, v in puzzle.parser.parse_known_args()[0].__dict__.items() if k != "func"}
        ns = argparse.Namespace(**{**outer_args, **inner_args})
        puzzle.run(ns)

parser.set_defaults(func=run_all_func)

args = parser.parse_args()
args.func(args)
