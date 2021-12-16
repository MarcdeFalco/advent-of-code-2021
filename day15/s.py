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

aoc = AOC(15)
si = aoc.input 
se = aoc.example

if submit:
    s = si
else:
    s = se

lines = s.split('\n')[:-1]

risk_0 = [ [ int(c) for c in l] for l in lines ]

def dec(l,x): return [(c+x)-9 if c+x > 9 else c+x for c in l ]
def dup(l): return sum((dec(l,i) for i in range(5)),[])

risk_1 = [ dup(l) for l in risk_0 ]
risk = sum(([ dec(l,i) for l in risk_1 ] for i in range(5)), [])
if part == 1: risk = risk_0
w, h = len(risk[0]), len(risk)

def voisins(x,y):
    for dx, dy in [ (1,0), (0,1), (-1,0), (0, -1) ]:
        if (dx,dy) != (0,0):
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h:
                yield (nx, ny)

from queue import PriorityQueue

tovisit = PriorityQueue()

total = [ [float('inf')]*w for _ in range(h) ]
visited = [ [False]*w for _ in range(h) ]
tovisit.put( (0, (0,0) ) )
total[0][0] = 0

pred = [ [ None ] * w for _ in range(h) ]

while not tovisit.empty():
    dist, (x, y) = tovisit.get()
    visited[y][x] = True

    for vx, vy in voisins(x,y):
        d = risk[vy][vx]
        if not visited[vy][vx]:
            old_risk = total[vy][vx]
            new_risk = total[y][x]+d
            if new_risk < old_risk:
                tovisit.put((new_risk, (vx,vy)))
                total[vy][vx] = new_risk
                pred[vy][vx] = (x,y)
    
lowest = total[h-1][w-1]
        
path = [ (w-1,h-1) ]

while path[-1] != (0,0):
    x, y = path[-1]
    path.append(pred[y][x])

if False:

    from PIL import Image

    im = Image.new('RGB', (w,h))

    for y in range(h):
        s = ''
        for x in range(w):
            v = risk[y][x]
            cv = int((v-1)/8*255)
            if (x,y) in path:
                im.putpixel( (x,y), (255,0,0) )
            else:
                im.putpixel( (x,y), (cv,cv,cv) )

    im.save('out.png')

ans = total[w-1][h-1]

if False:
    ans = 42

    lowest = [ [ 0 ] * w for _ in range(h) ]
    for x in range(w-1, -1, -1):
        for y in range(h-1, -1, -1):
            v = risk[y][x] 
            lv = [lowest[vy][vx] for (vx,vy) in voisins(x,y)]
            if lv != []:
                v += min(lv)
            lowest[y][x] = v

    ans = lowest[0][0] - risk[0][0]

if submit:
    pass
    #aoc.submit(part, ans)
else:
    print(ans)
