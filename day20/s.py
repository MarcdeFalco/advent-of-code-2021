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

aoc = AOC(20)
si = aoc.input 
se = aoc.example

if submit:
    s = si
else:
    s = se

s = s.split('\n')[:-1]

alg = list(s[0])

l_im = [ list(l) for l in s[2:] ]

im = defaultdict(bool)
for j, i in product(range(len(l_im)), range(len(l_im[0]))):
    if l_im[j][i] == '#':
        im[i,j] = True

def neighbors(im, i, j, inverted):
    b = '0b'
    for nj in range(j-1,j+2):
        for ni in range(i-1,i+2):
            if inverted:
                b += '0' if im[ni,nj] else '1'
            else:
                b += '1' if im[ni,nj] else '0'
    return eval(b)

def dim(im):
    i_s = [ i for (i,j) in im if im[i,j] ]
    j_s = [ j for (i,j) in im if im[i,j] ]
    return (min(i_s)-1, max(i_s)+1, min(j_s)-1, max(j_s)+1)

def evolve(im, src_inv, res_inv):
    im2 = defaultdict(bool)
    mi, Mi, mj, Mj = dim(im)
    for i, j in product(range(mi,Mi+1),range(mj,Mj+1)):
        v = neighbors(im, i, j, src_inv)
        c = '.' if res_inv else '#'
        if alg[v] == c:
            im2[i, j] = True
    return im2

def print_im(im, inv):
    mi, Mi, mj, Mj = dim(im)
    for j in range(mj,Mj+1):
        s = ''
        for i in range(mi,Mi+1):
            if (im[i,j] and not inv) or (not im[i,j] and inv):
                s += '#'
            else:
                s += '.'
        print(s)
            
if alg[0] == '#':
    odd, even = True, False
else:
    odd, even = False, False

for i in range(50):
    if i % 2 == 0:
        im = evolve(im, even, odd)
    else:
        im = evolve(im, odd, even)

ans = len(list((i,j) for (i,j) in im if im[i,j] ))



if submit:
    aoc.submit(part, ans)
else:
    print(ans)
