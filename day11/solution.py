from itertools import permutations, product, combinations
from collections import defaultdict, Counter
import sys
sys.path.append("..")
from speedaoc import AOC

aoc = AOC(11)

#s = aoc.example

s = open('example.txt').read()
m = [ [ int(c) for c in l ] for l in s.split('\n') if l != '']
w, h = len(m), len(m[0])

def voisins(x,y):
    for dx, dy in product(range(-1,2), repeat=2):
        if (dx,dy) != (0,0):
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h:
                yield (nx, ny)

NOT, TOFLASH, HASFLASHED = 0, 1, 2
def step():
    visited = defaultdict(int)
    toflash = []
    for x, y in product(range(w), range(h)):
        m[x][y] += 1
        if m[x][y] > 9:
            toflash.append((x, y))
            visited[x, y] = TOFLASH

    while toflash != []:
        x, y = toflash.pop()
        visited[x,y] = HASFLASHED
        for nx, ny in voisins(x,y):
            m[nx][ny] += 1
            if m[nx][ny] > 9 and visited[nx,ny] == NOT:
                toflash.append( (nx, ny) )
                visited[nx,ny] = TOFLASH

    count = 0
    for x, y in visited: # must be HASFLASHED
        m[x][y] = 0
        count += 1

    return count

all_flashed = w * h
count_flashed = 0
nsteps = 0
while True:
    nsteps+= 1
    count = step()
    if count == all_flashed:
        break
    count_flashed += count
    if nsteps == 100:
        print('Part 1', count_flashed)

print('Part 2', nsteps)
