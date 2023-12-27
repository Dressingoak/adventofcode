def contract(g, a):
    """Stoer-Wagner algorithm, contract step.

    Constract (merge) the least tightly connected node i g into the second least tightly
    connected node, starting from node a."""
    min_cut = 0
    s, A = a, set([a])
    while A != set(g):
        w = {}
        for n in A:
            for k, v in g[n].items():
                if k in A:
                    continue
                if k not in w:
                    w[k] = v
                else:
                    w[k] += v
        t = s
        A.add(s := max(w, key=w.get))
    g_new = {
        k: {kk: vv for kk, vv in v.items() if kk != t and kk != s}
        for k, v in g.items()
        if k != t and k != s
    }
    if isinstance(s, tuple) and isinstance(t, tuple):
        st = (*s, *t)
    elif isinstance(s, tuple):
        st = (*s, t)
    elif isinstance(t, tuple):
        st = (s, *t)
    else:
        st = (s, t)
    g_new[st] = {}
    for k, v in g.items():
        if k != s and k != t:
            w = sum((vv for kk, vv in v.items() if kk == s or kk == t), 0)
            if w > 0:
                g_new[k][st] = w
        if k == s:
            min_cut = sum(v.values(), 0)
    ww = {}
    for k, v in g_new.items():
        w = next((vv for kk, vv in v.items() if kk == st), None)
        if w is not None:
            ww[k] = w
    g_new[st] = ww
    return min_cut, g_new, s


def minimum_cut(g, a=None):
    """Stoer-Wagner algorithm, main loop.

    Contract all nodes of g and find the minimum cut that partitions g into two
    disjoint graphs."""
    min_cut, s = None, None
    all_keys = set(g)
    if a is None:
        a = next(iter(g))
    # g_all = len(g)
    while len(g) > 1:
        # print(f"{g_all-len(g)}/{g_all-1} ({(g_all-len(g)) / (g_all-1) * 100:.2f}%)")
        min_cut_next, g, s_next = contract(g, a)
        if min_cut is None or min_cut_next <= min_cut:
            min_cut = min_cut_next
            s = s_next
    # print(f"{g_all-len(g)}/{g_all-1} ({(g_all-len(g)) / (g_all-1) * 100:.2f}%)")
    ss = set(s) if isinstance(s, tuple) else set([s])
    return min_cut, ss, all_keys.difference(ss)


def parse(file: str):
    G = {}
    with open(file) as f:
        for line in f:
            src, dsts = line.strip().split(": ")
            for dst in dsts.split(" "):
                if src not in G:
                    G[src] = {dst: 1}
                else:
                    G[src][dst] = 1
                if dst not in G:
                    G[dst] = {src: 1}
                else:
                    G[dst][src] = 1
    return G


def part1(file: str):
    G = parse(file)
    _, s1, s2 = minimum_cut(G)
    return len(s1) * len(s2)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
