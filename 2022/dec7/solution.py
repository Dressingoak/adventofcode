import sys
sys.path.append('../')
from timing import print_timing

def find(dir, path: list[str]):
    match path:
        case []: return dir,
        case [p, *rest]: return find(dir[p], rest)

def dir_size(dir, sizes, prefix=""):
    s = 0
    for d, content in dir.items():
        if isinstance(content, int):
            s += content
        else:
            folder = prefix + d
            size = dir_size(content, sizes, folder + ("/" if d != "/" else ""))
            sizes[folder] = size
            s += size
    return s

def get_all_dir_sizes(file: str):
    with open(file, "r") as f:
        cur, files = [], {}
        for line in f.readlines():
            match line.strip().split():
                case ["$", "cd", "/"]: cur = []
                case ["$", "cd", ".."]: cur.pop()
                case ["$", "cd", dir]: cur.append(dir)
                case ["$", "ls"]: content = True
                case ["dir", dir]:
                    loc, = find(files, cur)
                    if not dir in loc:
                        loc[dir] = {}
                case [size, f]:
                    loc, = find(files, cur)
                    loc[f] = int(size)
    contents = {}
    dir_size({"/": files}, contents)
    return contents

@print_timing
def calculate_part1(file: str):
    contents = get_all_dir_sizes(file)
    return sum(s for s in contents.values() if s <= 100000)

@print_timing
def calculate_part2(file: str):
    contents = get_all_dir_sizes(file)
    needed = 30000000 - (70000000 - contents["/"])
    return min(s for s in contents.values() if s >= needed)
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 7, part 1: {} (took {})".format(*calculate_part1(file)))
    print("Dec 7, part 2: {} (took {})".format(*calculate_part2(file)))
