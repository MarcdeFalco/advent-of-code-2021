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

aoc = AOC(13)
si = aoc.input 
se = aoc.example

if submit:
    s = si
else:
    s = se

s = si
paper = defaultdict(bool)
folds = []
for l in s.split('\n'):
    if l == '': continue
    if l.startswith('fold'):
        i = l.index('=')
        folds.append( (l[i-1], int(l[i+1:])) )
    else:
        a, b = map(int, l.split(','))
        paper[a,b] = True

d,n = folds[0]

def fold(paper,d,n):
    paperf = defaultdict(bool)
    if d == 'y':
        for (x,y) in paper:
            if y < n:
                paperf[x,y] = paper[x,y]
            else:
                paperf[x,n-(y-n)] = paper[x,y]
    else:
        for (x,y) in paper:
            if x < n:
                paperf[x,y] = paper[x,y]
            else:
                paperf[n-(x-n),y] = paper[x,y]
    return paperf
for d, n in folds:
    paper = fold(paper,d,n)

for y in range(50):
    s = ''
    for x in range(100):
        if paper[x,y]:
            s += '#'
        else:
            s += '.'
    print(s)


if submit:
    aoc.submit(part, ans)
else:
    print(ans)
