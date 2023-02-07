import argparse
import importlib

modules = {day: importlib.import_module(f"dec{day}.solution") for day in range(1, 26)}

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
subparsers = parser.add_subparsers()

for day, module in modules.items():
    subparser = subparsers.add_parser(f"{day}", help=f'run solution(s) for Dec {day} {module.puzzle.year}', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    module.puzzle.build_parser(subparser)
    def run():
        module.puzzle.run
    subparser.set_defaults(func=module.puzzle.run)

args = parser.parse_args()
args.func(args)
