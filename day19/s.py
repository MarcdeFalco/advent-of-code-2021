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

aoc = AOC(19)
si = aoc.input 
se = aoc.example

if submit:
    s = si
else:
    s = se

ans = 42

s = s.split('\n')[:-1]

i = 0
scanners = []
while i < len(s):
    if s[i][:3] != '---':
        raise ValueError

    i += 1
    scanner = []
    while i < len(s) and s[i] != '':
        scanner.append(eval(s[i]))
        i += 1
    scanners.append(scanner)
    i += 1

# Enumerate direct space orientations
configurations = []
for x, sig in product(range(3), [-1,1]):
    y = (x+1*sig) % 3
    z = (x+2*sig) % 3
    configurations += [
        ( (x,sig), (y,1), (z,1) ),
        ( (x,sig), (z,1), (y,-1) ),
        ( (x,sig), (y,-1), (z,-1) ),
        ( (x,sig), (z,-1), (y,1) )
        ]

def perm(t, config):
    (a1,s1), (a2,s2), (a3,s3) = config
    return (s1 * t[a1], s2 * t[a2], s3 * t[a3])

def permute(scanner, config):
    return [ perm(t,config) for t in scanner ]

def intersection(s1, s2):
    i = []
    for c in s1:
        if c in s2:
            i.append(c)
    return i

def diff(b,b1):
    return (b[0]-b1[0],b[1]-b1[1],b[2]-b1[2])
def add(b,b1):
    return (b[0]+b1[0],b[1]+b1[1],b[2]+b1[2])

def align(as1, s2, ib2):
    b2 = s2[ib2]
    as2 = [ diff(b,b2) for b in s2 ]

    m = defaultdict(int)
    for c in as1:
        m[c]+=1
    for c in as2:
        m[c]+=1

    i = []
    for c in m:
        if m[c] == 2:
            i.append(c)

    return i

nscanners = len(scanners)
conf_found = { 0 : configurations[0] }
pos_found = { 0 : (0,0,0) }

def translate(a,b,c):
    v = []
    for i in range(3):
        v.append( a[i] - b[i] + c[i] )
    return tuple(v)

matches = []

preprocess = []
for si, s in enumerate(scanners):
    l = {}
    for i, c in enumerate(configurations):
        sc = permute(s, c)
        for ib, b in enumerate(s):
            l[c,ib] = [ diff(ob, b, sc) for ob in sc ]
    preprocess.append(l)

if matches == []:
    to_pairs = list(range(1,nscanners)) 
    to_visit = [ 0 ]

    while to_visit != []:
        is1 = to_visit.pop()
        s1  = scanners[is1]
        new_to_pairs = to_pairs[:]

        for is2 in to_pairs:
            print(is1, is2)

            s2  = scanners[is2]

            for c in configurations:
                match = None
                sc1 = s1
                sc2 = permute(s2,c)

                for ib1 in range(len(s1)):
                    b1 = sc1[ib1]

                    for ib2 in range(len(s2)):
                        b2 = sc2[ib2]
                        as2 = [ translate(b, b2, b1) for b in sc2 ]
                        i = set(sc1).intersection(set(as2))

                        if len(i) >= 12:
                            match = (is1, ib1, is2, ib2, c, len(i))
                            matches.append(match)

                            p = pos_found[is1]
                            p2 = translate(p, b2, b1)

                            pos_found[is2] = p2
                            print(is2, p2)

                            scanners[is2] = sc2

                            to_visit.append(is2)
                            new_to_pairs.remove(is2)

                            break

                    if match is not None:
                        break

                if match is not None:
                    break


        to_pairs = new_to_pairs

    print(repr(matches))

beacons = []
for i in range(nscanners):
    for b in scanners[i]:
        tb = add(b, pos_found[i])
        if tb not in beacons:
            beacons.append(tb)
print(len(beacons))

print(pos_found)

#if submit:
#    aoc.submit(part, ans)
#else:
#    print(ans)
