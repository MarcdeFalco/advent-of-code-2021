import sys
sys.path.append("..")
from speedaoc import AOC

aoc = AOC(5)

s = aoc.example #the daily input is stored in s
s = aoc.input 

s = open('input.txt').read().strip()
m = {}

for l in s.split('\n'):
    a, b = l.split(' -> ')
    x1, y1 = map(int, a.split(','))
    x2, y2 = map(int, b.split(','))

    if x1 == x2:
        if y1 > y2:
            y1, y2 = y2, y1
        for y in range(y1, y2+1):
            m[x1, y] = m.get((x1,y), 0) + 1
    elif y1 == y2:
        if x1 > x2:
            x1, x2 = x2, x1
        for x in range(x1, x2+1):
            m[x, y1] = m.get((x,y1), 0) + 1
    else:
        coeff = (x2 - x1) / (y2 - y1)
        if coeff in [ 1., -1. ]:
            if x1 > x2:
                x1, x2, y1, y2 = x2, x1, y2, y1
            for k in range(x2-x1+1):
                nx, ny = x1+k, y1+coeff*k
                m[nx, ny] = m.get((nx,ny), 0) + 1

count = 0
for c in m:
    if m[c] > 1:
        count += 1

print('Part 2', count)
