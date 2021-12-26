from copy import copy, deepcopy
from itertools import permutations, product, combinations
from collections import defaultdict, Counter
import sys
sys.path.append("..")
from speedaoc import AOC
import pyxel

submit = False
if 'submit' in sys.argv:
    submit = True
part = 1
if '2' in sys.argv:
    part = 2

print(submit, part)

aoc = AOC(25)
si = aoc.input
s = aoc.example

if submit:
    s = si

class Map:
    def __init__(self, w, h, data=None):
        if data is not None:
            self.data = data
        else:
            self.data = [ [ '.' ] * w for _ in range(h) ]
        self.w = w
        self.h = h

    def __getitem__(self, c):
        x, y = c
        return self.data[y % self.h][x % self.w]

    def __setitem__(self, c, v):
        x, y = c
        self.data[y % self.h][x % self.w] = v

    def coords(self):
        return product(range(self.w), range(self.h))

s = [ list(v) for v in s.split('\n')[:-1] ]
w = len(s[0])
h = len(s)

m = Map(w, h, s)
print(w,h,s)

def move(m, tgt, delta):
    nm = Map(m.w,m.h)
    for x, y in m.coords():
        if m[x,y] == tgt and m[delta(x,y)] == '.':
            nm[delta(x,y)] = tgt
        elif m[x,y] != '.':
            nm[x,y] = m[x,y]
    return nm

def right(x,y): return (x+1,y)
def down(x,y): return (x,y+1)

def evolve(m):
    m = move(m, '>', right)
    m = move(m, 'v', down)
    return m

ans = 0
while True:
    nm = evolve(m)
    ans += 1

    #print(ans, 'steps')
    #for l in nm.data:
    #    print(''.join(l))

    if m.data == nm.data:
        break
    m = nm

if submit:
    aoc.submit(part, ans)
else:
    print(ans)
