import os
from pathlib import Path
import time
from functools import wraps
import statistics
import argparse
import inspect

class Colors:
    '''Colors class:reset all colors with colors.reset; two
    sub classes fg for foreground
    and bg for background; use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.greenalso, the generic bold, disable,
    underline, reverse, strike through,
    and invisible work with the main class i.e. colors.bold'''
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
 
    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'
 
    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


def timeit(func, repeat_atleast):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_outer = time.perf_counter()
        end_outer = None
        durations = []
        while end_outer is None or end_outer - start_outer < repeat_atleast:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            durations.append(end - start)
            end_outer = end
        if len(durations) > 1:
            return (result, min(durations), statistics.stdev(durations), len(durations))
        else:
            return (result, durations[0], None, 1)
    return wrapper


class Puzzle(object):

    def add_general_group(parser):
        general_args = parser.add_argument_group('general', 'arguments applicable to the execution of the puzzle')
        general_args.add_argument("-c", "--color", action=argparse.BooleanOptionalAction, help="add color to output information", default=True)
        general_args.add_argument("-r", "--result-only", dest="result_only", action="store_true", help="only print the result", default=False)
        general_args.add_argument("-b", "--benchmark", metavar="DURATION", help="repeat the method for at least DURATION seconds", default=0.0, type=float)

    def __init__(self, script: str, use_defaults: bool = True):
        path = Path(script)
        self.script = script
        self.day = int(path.parent.name[3:])
        self.year = int(path.parent.parent.name)
        self.arguments = {}
        self.callables = {}
        self.use_defaults = use_defaults

        cwd = os.getcwd()
        self.defaults = {
            "file": {"help": "file to process", "default": self.resolve_relative_path("input.txt")}
        }
        self.parser = None

    def resolve_relative_path(self, file: str):
        cwd = os.getcwd()
        return os.path.relpath(os.path.join(os.path.dirname(self.script), file), cwd)

    def add_part(self, part: int, func):
        signature = inspect.signature(func)

        # Add methods
        self.callables[part] = {
            "name": func.__name__,
            "callable": func,
            "args": list(signature.parameters.keys())
        }

        # Add parameters
        for param in signature.parameters.values():
            name = param.name
            kwargs = {k: v for k, v in {"desc": None, "default": param.default if param.default is not inspect._empty else None}.items() if v is not None}
            if name not in self.arguments:
                self.arguments[name] = {
                    "parts": set([part]),
                    "kwargs": kwargs
                }
            else:
                if self.arguments[name]["kwargs"] == kwargs:
                    self.arguments[name]["parts"].add(part)
                else:
                    raise RuntimeError(f"""Function parameter '{name}' of function '{func.__name__}' carry different kwargs: {kwargs} (new) != {self.arguments[name]["kwargs"]} (existing).""")

    def get_parameter_kwargs(self, name: str) -> dict:
        return self.arguments[name]["kwargs"]

    def set_parameter_help(self, name: str, help: str):
        self.arguments[name]["kwargs"]["help"] = help

    def set_parameter_type_bool(self, name: str):
        self.arguments[name]["kwargs"]["action"] = "store_true"

    def set_parameter_resolve_path(self, name: str, arg: str = "default"):
        value = self.arguments[name]["kwargs"][arg]
        self.arguments[name]["kwargs"][arg] = self.resolve_relative_path(value)

    def build_parser(self, parser = None):
        if parser is None:
            self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            Puzzle.add_general_group(self.parser)
        else:
            self.parser = parser

        # Apply defaults to arguments
        if self.use_defaults:
            for param, kwargs in self.defaults.items():
                if param in self.arguments:
                    for k, v in kwargs.items():
                        if k not in self.arguments[param]["kwargs"]:
                            self.arguments[param]["kwargs"][k] = v
        for param, properties in self.arguments.items():
            parts = ", ".join(str(_) for _ in sorted(list(properties["parts"])))
            if "help" in properties["kwargs"]:
                properties["kwargs"]["help"] += f" (applies to parts: {parts})"
            else:
                properties["kwargs"]["help"] = f"applies to parts: {parts}"

        # Arguments that applies to the CLI itself
        parts = [part for part in sorted(_ for _ in self.callables.keys())]
        self.parser.add_argument("-p", "--parts", nargs="+", choices=parts, help="parts to run", default=parts, type=int)

        # Arguments that applies to the individual parts
        specific_args = self.parser.add_argument_group('specific', 'arguments applicable to the specific calculations')
        for param, properties in self.arguments.items():
            kwargs = properties["kwargs"]
            specific_args.add_argument(f"--{param}", **kwargs)

    def run(self, args = None):
        if self.parser is None:
            self.build_parser()
        if args is None:
            args = self.parser.parse_args()
        
        for part in args.parts:
            part = part
            parameters = {k: v for k, v in args.__dict__.items() if k in self.callables[part]["args"]}
            if args.result_only:
                result = self.callables[part]["callable"](**parameters)
                print(result)
            else:
                result, duration, sd, n = timeit(self.callables[part]["callable"], args.benchmark)(**parameters)
                self.print_formatted_result(args.color, part, result, duration, sd, n)

    def print_formatted_result(self, colored: bool, part, result, duration, sd, n):
        def format_duration(duration):
            match duration:
                case duration if duration * 1_000 < 1: return '{:.3f} μs'.format(duration*1_000_000)
                case duration if duration < 1: return '{:.3f} ms'.format(duration*1_000)
                case duration: return '{:.3f} s'.format(duration)
        fmt_pre = f"Dec {self.day}, part {part}: "
        print(Colors.fg.yellow, fmt_pre, sep="", end="") if colored else print(fmt_pre, end="")
        fmt_res = f"{result} "
        print(Colors.reset, fmt_res, sep="", end="") if colored else print(fmt_res, end="")
        fd = format_duration(duration)
        if sd is not None:
            fsd = format_duration(sd)
            fmt_time = f"(took at best {fd}, {fsd} spread, {n} repeats)"
        else:
            fmt_time = f"(took {fd})"
        print(Colors.fg.black, fmt_time, Colors.reset, sep="") if colored else print(fmt_time)
