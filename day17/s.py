from itertools import permutations, product, combinations
from collections import defaultdict, Counter
import sys
sys.path.append("..")
from speedaoc import AOC

submit = False
if 'submit' in sys.argv:
    submit = True
part = 1
if '2' in sys.argv:
    part = 2

print(submit, part)

aoc = AOC(17)
si = aoc.input 
se = aoc.example

if submit:
    s = si
else:
    s = se

import re
r = re.compile(r'target area: x=(?P<xlow>.*)\.\.(?P<xhigh>.*), y=(?P<ylow>.*)\.\.(?P<yhigh>.*)')

m = r.match(s)
xlow, xhigh, ylow, yhigh = map(int, m.groups())

best = (0,0), 0

possible = []
for xi0 in range(xhigh+1):
    for yi0 in range(ylow,-ylow):
        init = xi0,yi0
        xi = xi0
        yi = yi0
        x, y = 0, 0
        maxy = 0
        while y >= ylow:
            x += xi
            y += yi
            if y > maxy: maxy = y
            if xi > 0: xi -= 1
            elif xi < 0: xi += 1
            yi -= 1

            if xlow <= x <= xhigh and ylow <= y <= yhigh:
                pos, gmax = best
                if maxy > gmax:
                    best = (init, maxy)
                possible.append(init)


toget = []
for l in open('target'):
    points = [ eval('('+c+')') for c in  l.strip().split() ]
    toget += points

possible = list(set(possible))

ans = len(possible)

if submit:
    aoc.submit(part, ans)
else:
    print(ans)
