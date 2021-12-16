from itertools import permutations
import sys
sys.path.append("..")
from speedaoc import AOC

aoc = AOC(10)

s = aoc.input 
s = open('example.txt').read()

o = { '(':')','[':']','{':'}','<':'>'}
def check(s):
    p = []
    for c in s:
        if c in '([{<':
            p.append(o[c])
        else:
            try:
                x = p.pop()
                if x != c:
                    return c
            except IndexError:
                return c
    return p

score = { ')' : 3, ']' : 57, '}': 1197, '>': 25137 }
sum1 = 0
sum2 = []
for l in s.split('\n'):
    l = l.strip()
    if l == '': continue
    c = check(l)
    if type(c) == str:
        sum1 += score[c]
    else:
        c.reverse()
        sc = 0
        for ch in c:
            sc = 5 * sc + ')]}>'.index(ch) + 1
        sum2.append(sc)

sum2.sort()
print('Part1',  sum1)
print('Part2',  sum2[len(sum2)//2])

#aoc.submit(2, ans)
