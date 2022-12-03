import sys
sys.path.append("..")
from speedaoc import AOC

aoc = AOC(6)

s = aoc.example #the daily input is stored in s
s = aoc.input 

fish = list(map(int, s.split(',')))

fmap = [ 0 ] * 9
for f in fish:
    fmap[f] += 1

for days in range(256):
    nmap = [ 0 ] * 9
    newfish = 0
    for i in range(8):
        nmap[i] = fmap[i+1]

    nmap[8] += fmap[0]
    nmap[6] += fmap[0]

    fmap = nmap

ans = sum(fmap)

aoc.submit(2, ans)
