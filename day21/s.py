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

aoc = AOC(21)

if submit:
    pos = [ 7, 10 ]
else:
    pos = [ 4, 8 ]

def dice_det_100():
    n = 0
    while True:
        yield (n+1)
        n = (n+1) % 100 

splits = Counter(map(sum,product(range(1,4),repeat=3)))

cache = {}
def experiments(p, scores, pos):
    code = (p,)+tuple(scores)+tuple(pos)
    if code in cache:
        return cache[code]
    if scores[0] >= 21:
        cache[code] = [1,0]
        return [1, 0]
    if scores[1] >= 21:
        cache[code] = [0,1]
        return [0, 1]
    wins = [ 0, 0 ]
    for d in splits:
        c = splits[d]
        npos = pos[:]
        nscores = scores[:]
        npos[p] = 1 + (pos[p]+d-1) % 10
        nscores[p] += npos[p]
        np = (p+1)%2
        for i in range(2):
            ewin = experiments(np, nscores, npos)
            wins[i] += c * ewin[i]
    cache[code]  = wins
    return wins

ans = max(experiments(0, [0,0], pos))

if submit:
    aoc.submit(part, ans)
else:
    print(ans)
