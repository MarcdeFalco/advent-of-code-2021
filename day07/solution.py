import sys
sys.path.append("..")
from speedaoc import AOC

aoc = AOC(8)

#the daily input is stored in s
s = aoc.example 
s = aoc.input 
part2 = True

pos = list(map(int, s.split(',')))

m = max(pos)

costs = []
for i in range(m):
    c = 0
    for p in pos:
        d =  abs(p-i)
        if part2:
            c += (d*(d+1))//2
        else:
            c += d
    costs.append(c)
tgt = min(costs)
print(tgt)

ans = tgt

#aoc.submit(2, ans)
