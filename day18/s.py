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

aoc = AOC(18)
si = aoc.input 
se = aoc.example

if submit:
    s = si
else:
    s = se

ans = 42

snails = s.split('\n')[:-1]

def add(s1,s2):
    return '['+s1+','+s2+']'

debug = False

def reduce_explode(s):
    level = 0
    pair1 = None
    i = 0
    while i < len(s):
        c = s[i]
        if c == '[':
            level += 1
            pair1 = None
        elif c == ']':
            level -= 1
            pair1 = None
        elif c == ',':
            pass
        elif pair1 is None:
            start = i
            n = c
            while i < len(s)-1 and s[i+1].isdigit():
                i += 1
                n += s[i]
            pair1 = start, int(n)
        else:
            n = c
            while i < len(s)-1 and s[i+1].isdigit():
                i += 1
                n += s[i]
            n2 = int(n)
            start, n1 = pair1
            if level > 4:
                return explode(s, start, i+1, n1, n2)
        i += 1
    return s

def add_left(s, a):
    i = len(s)-1
    l = ''
    while i >= 0:
        c = s[i]
        if c.isdigit():
            n = c
            while i > 0 and s[i-1].isdigit():
                i -= 1
                n = s[i] + n
            return s[:i] + str(int(n)+a) + l
        else:
            l = c + l
        i -= 1
    return s

def add_right(s, a):
    i = 0
    l = ''
    while i < len(s):
        c = s[i]
        if c.isdigit():
            n = c
            while i < len(s)-1 and s[i+1].isdigit():
                i += 1
                n = n + s[i]
            return l + str(int(n)+a) + s[i+1:]
        else:
            l = l + c
        i += 1
    return s

def explode(s, i, j, n1, n2):
    if debug:
        print(s[:i-1], '{', s[i-1:j+1], '}', s[j+1:])
        print(add_left(s[:i-1], n1), '{', s[i-1:j+1], '}',
                add_right(s[j+1:],n2))
    return add_left(s[:i-1], n1) + '0' + add_right(s[j+1:], n2)

def reduce_split(s):
    i = 0
    while i < len(s):
        start = i
        c = s[i]
        if c.isdigit():
            n = c
            while i < len(s)-1 and s[i+1].isdigit():
                i += 1
                n += s[i]
            n = int(n)
            if n >= 10:
                if n % 2 == 0:
                    a, b = n//2, n//2
                else:
                    a, b = n//2, 1 + n//2
                if debug:
                    print(s[:start], '{', n, '->', (a,b), '}', s[i+1:])
                return s[:start] + '[' + str(a) + ','+str(b)+']' + s[i+1:]
        i += 1
    return s


def reduce(s):
    reduced = False
    steps = 0
    while not reduced:
        rs = reduce_explode(s)
        if rs == s:
            rs = reduce_split(s)

        if rs != s:
            s = rs
        else:
            reduced = True

        steps += 1


    return s

s = snails[0]
for os in snails[1:]:
    s = reduce(add(s, os))


s = eval(s)
def magnitude(s):
    if type(s) == int:
        return s
    a, b = s
    return 3 * magnitude(a) + 2 * magnitude(b)

ans = magnitude(s)

max_mag = None
for i1 in range(len(snails)):
    for i2 in range(i1+1, len(snails)):
        s1 = snails[i1]
        s2 = snails[i2]

        for i in range(2):
            m = magnitude(eval(reduce(add(s1,s2))))
            if max_mag is None or m > max_mag:
                max_mag = m
            s2, s1 = s1, s2

ans = max_mag

if submit:
    aoc.submit(part, ans)
else:
    print(ans)
