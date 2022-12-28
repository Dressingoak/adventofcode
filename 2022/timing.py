import time
from functools import wraps

def print_timing(func):
    '''
    create a timing decorator function
    use
    @print_timing
    just above the function you want to time
    '''
    @wraps(func)  # improves debugging
    def wrapper(*arg):
        start = time.perf_counter()
        result = func(*arg)
        end = time.perf_counter()
        match (end - start):
            case duration if duration * 1_000 < 1: fs = '{:.3f} μs'.format(duration*1_000_000)
            case duration if duration < 1: fs = '{:.3f} ms'.format(duration*1_000)
            case duration: fs = '{:.3f} s'.format(duration)
        return result, fs
    return wrapper
