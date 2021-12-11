from itertools import permutations, product, combinations
from collections import Counter, defaultdict
import sys
sys.path.append("..")
from speedaoc import AOC

#aoc = AOC(9)

l = [ l.strip() for l in open('example.txt') ]
l = [ l.strip() for l in open('input.txt') ]

w, h = len(l[0]), len(l)

low = []

risk = 0
for x in range(w):
    for y in range(h):
        v = []
        for dx in range(x-1,x+2):
            for dy in range(y-1,y+2):
                if (dx == x and dy != y) or (dy == y and dx != x):
                    if 0 <= dx < w and 0 <= dy < h:
                        v.append(int(l[dy][dx]))

        m = min(v)
        r = int(l[y][x])
        if m > r:
            low.append((x,y))
            risk += 1+r

print('Part 1', risk)

basins = []
for x, y in low:
    basin = []
    tovisit = [ (x,y) ]
    while tovisit != []:
        x, y = tovisit.pop()
        basin.append( (x,y) )
        for dx in range(x-1,x+2):
            for dy in range(y-1,y+2):
                if (dx == x and dy != y) or (dy == y and dx != x):
                    if 0 <= dx < w and 0 <= dy < h:
                        v=int(l[dy][dx])
                        if v != 9 and (dx,dy) not in basin and (dx, dy) not in tovisit:
                            tovisit.append( (dx, dy) )

    basins.append( len(basin))

basins.sort()
a, b, c = basins[-3:]
print('Part 2', a*b*c)
