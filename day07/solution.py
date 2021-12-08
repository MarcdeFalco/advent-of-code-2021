import sys
sys.path.append("..")
from speedaoc import AOC

aoc = AOC(8)

s = aoc.example #the daily input is stored in s
s = aoc.input 

pos = list(map(int, s.split(',')))

m = max(pos)

costs = []
for i in range(m):
    c = 0
    for p in pos:
        d =  abs(p-i)
        c += (d*(d+1))//2
    costs.append(c)
tgt = min(costs)
print(costs.index(tgt))
print(tgt)

ans = tgt

aoc.submit(2, ans)
