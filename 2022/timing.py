from pathlib import Path
import time
from functools import wraps
import click
from click import Command

def print_timing(func):
    '''
    create a timing decorator function
    use
    @print_timing
    just above the function you want to time
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        obj = args[0]
        start = time.perf_counter()
        result = func(*args[1:], **kwargs)
        end = time.perf_counter()
        part = int(func.__name__[-1])
        obj.format_result(part, result, start, end)
        return result
    return wrapper

class Puzzle(object):
    def __init__(self, script: str):
        path = Path(script)
        self.day = int(path.parent.name[3:])
        self.year = int(path.parent.parent.name)

    def format_result(self, part, result, start, end):
        match (end - start):
            case duration if duration * 1_000 < 1: fs = '{:.3f} μs'.format(duration*1_000_000)
            case duration if duration < 1: fs = '{:.3f} ms'.format(duration*1_000)
            case duration: fs = '{:.3f} s'.format(duration)
        click.secho(f"Dec {self.day}, part {part}: ", fg='yellow', nl=False)
        click.echo(f"{result} ", nl=False)
        click.secho(f"(took {fs})", fg='black') 

def setup_cli(script: str, *commands: Command):
    def apply_options(func, options: dict[str, tuple[str, str]]):
        if len(options) == 0:
            return func
        name, (default, help) = options.popitem()
        f = (click.option(f'--{name}', default=default, help=help))(func)
        return apply_options(f, options)

    options = dict()

    @click.group()
    @click.pass_context
    def cli(ctx):
        ctx.obj = Puzzle(script)
    
    for command in commands:
        for param in command.params:
            options[param.name] = (param.default, param.help)
        cli.add_command(command)

    @click.command()
    @click.pass_context
    def run(ctx, **kwargs):
        for command in commands:
            ctx.forward(command)

    run_with_args = apply_options(run, options)

    cli.add_command(run_with_args)
    return cli
