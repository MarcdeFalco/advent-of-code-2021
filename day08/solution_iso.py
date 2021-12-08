from itertools import product

def count_ones(n):
    return bin(n).count('1')

def get_one(n):
    k = 0
    while n != 1:
        n //= 2
        k += 1
    return k

def tonum(p):
    s = 0
    for c in p:
        j = ord(c) - ord('a')
        s += 1 << j
    return s

def sortstr(s):
    return ''.join(sorted(s))

def sig(ps):
    nums = [ tonum(p) for p in ps ]
    g = {}
    for n1, n2 in product(nums, repeat=2):
        i = count_ones(n1 & n2)
        g[n1,n2] = g[n2,n1] = i
    deg = [ sum(g[n,m] for m in nums) for n in nums ]
    return deg

digits = [ 'abcefg', 'cf', 'acdeg', 'acdfg',
    'bcdf', 'abdfg', 'abdefg', 'acf',
    'abcdefg', 'abcdfg' ]

g0 = sig(digits)
answer = 0

for l in open('input.txt'):
    if l == '': break

    patterns = [ sortstr(v) for v in l.split(' | ')[0].split() ]
    tgts = [ sortstr(v) for v in l.split(' | ')[1].split() ]

    g = sig(patterns)

    num = int(''.join(str(g0.index(g[patterns.index(tgt)])) for tgt in tgts))

    answer += num

print('Part 2', answer)
