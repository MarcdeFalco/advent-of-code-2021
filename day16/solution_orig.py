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

aoc = AOC(16)
si = aoc.input 
se = aoc.example

if submit:
    s = si
else:
    s = se

from struct import unpack, pack
s = s.strip()
def bits(s):
    for i in range(len(s)):
        c = eval('0x'+s[i])
        cb = bin(c)[2:]
        cb = '0'*(4-len(cb)) + cb
        for b in cb:
            yield b

g = bits(s)

def read_nbit(n):
    s = ''
    for i in range(n):
        s += next(g)
    return eval('0b'+s)

def read_packet():
    version = read_nbit(3)
    pid = read_nbit(3)
    read = 6
    if pid == 4:
        num = 0
        while True:
            sG = read_nbit(1)
            g = read_nbit(4)
            read += 5
            num = num * 16 + g
            if sG == 0: break
        return { 'read' : read, 'version' : version, 'pid' : pid, 'sub' : [],'num' : num }
    else:
        lid = read_nbit(1)
        read += 1
        sub = []
        if lid == 0:
            length = read_nbit(15)
            read += 15 + length
            while length > 0:
                p = read_packet()
                sub.append(p)
                length -= p['read']
        else:
            num = read_nbit(11)
            read += 11
            for _ in range(num):
                p = read_packet()
                sub.append(p)
                read += p['read']

        return { 'read' : read, 'version' : version, 'pid' : pid, 'sub' : sub }

p = read_packet()

def somme_version(p):
    return p['version'] + sum(somme_version(sp) for sp in p['sub'])

import math
def value(p):
    if p['pid'] == 4:
        return p['num']
    op = { 0: sum, 1 : math.prod, 2 : min, 3 : max }
    if p['pid'] in op:
        return op[p['pid']](value(sp) for sp in p['sub'])
    a, b = map(value, p['sub'])
    if p['pid'] == 5 and a > b:
        return 1
    if p['pid'] == 7 and a == b:
        return 1
    if p['pid'] == 6 and a < b:
        return 1
    return 0

ans = value(p)

if submit:
    aoc.submit(part, ans)
else:
    print(ans)
