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

aoc = AOC(14)
si = aoc.input 
se = aoc.example

if submit:
    s = si
else:
    s = se

lines = s.split('\n')[:-1]
mol = lines[0]
instr = lines[2:]

subst = {}
for l in instr:
    pair, ins = l.split(' -> ')
    subst[pair] = ins


def replace(s):
    o = ''
    for i in range(len(s)-1):
        v = s[i]+s[i+1]
        o += s[i]
        if v in subst:
            o += subst[v]
    o += s[-1]
    return o

for step in range(10):
    mol = replace(mol)

c = Counter(mol)
l = c.most_common(26)

ans = l[0][1] - l[-1][1]

synth = defaultdict(int)
mol = lines[0]
for i in range(len(mol)-1):
    synth[mol[i]+mol[i+1]] += 1

def step(synth):
    nsynth = defaultdict(int)
    for pair in synth:
        if pair in subst:
            nsynth[pair[0]+subst[pair]] += synth[pair]
            nsynth[subst[pair]+pair[1]] += synth[pair]
        else:
            nsynth[pair] += synth[pair]
    return nsynth

for i in range(40):
    synth = step(synth)

c = Counter()
for pair in synth:
    c[pair[0]]+=synth[pair]
    c[pair[1]]+=synth[pair]

l = c.most_common(26)
ans = (l[0][1] - l[-1][1])//2+1

if submit:
    aoc.submit(part, ans)
else:
    print(ans)
