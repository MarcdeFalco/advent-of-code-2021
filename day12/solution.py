from itertools import permutations, product, combinations
from collections import defaultdict, Counter
import sys
sys.path.append("..")
from speedaoc import AOC

aoc = AOC(12)

s = aoc.example
s = aoc.input

def read_graph(s):
    gr = defaultdict(list)
    for l in s.split('\n'):
        if l == '': break
        a, b = l.split('-')
        gr[a].append(b)
        gr[b].append(a)
    return gr

gr = read_graph(open('input.txt').read())

def visit(x, smalls, double=False):
    n_paths = 0
    for v in gr[x]:
        if v == 'start': continue
        if v == 'end': n_paths += 1
        elif v.islower(): # small cave
            if v in smalls and not double:
                n_paths += visit(v, smalls, True)
            elif not v in smalls:
                n_paths += visit(v, smalls.union([v]), double)
        else:
            n_paths += visit(v, smalls, double)
    return n_paths

ans = visit('start', set(), True)
print('Part 1', ans)
ans = visit('start', set())
print('Part 2', ans)

#aoc.submit(1, ans)
#aoc.submit(2, ans)
