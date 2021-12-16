import sys
sys.path.append("..")
from speedaoc import AOC

aoc = AOC(8)

l = aoc.input .split('\n')
#l = aoc.example.split('\n')

N = len(l)
num = 0
for i in range(N):
    pwires = [ 'abcefg', 'cf', 'acdeg', 'acdfg',
            'bcdf', 'abdfg', 'abdefg', 'acf',
            'abcdefg', 'abcdfg']

    if l[i] == '':
        break
    patterns = l[i].split(' | ')[0].split()
    tgts = l[i].split(' | ')[1].split()

    cor = {}

    pbyl = {}
    for p in patterns:
        pbyl[len(p)] = pbyl.get(len(p), []) + [ p ]

    p1 = pbyl[2][0]
    p7 = pbyl[3][0]


    for c in p7:
        if c not in p1:
            cor[c] = 'a'


    for p in pbyl[6]:
        not_in_1 = None
        for c in p1:
            if c not in p:
                not_in_1 = c
                break
        if not_in_1 is not None:
            break

    cor[not_in_1] = 'c'
    cor[[ c for c in p1 if c != not_in_1 ][0]] = 'f'

    npbyl = {}
    for n in pbyl:
        rem = list(cor.keys())
        for p in pbyl[n]:
            s = ''
            for c in p:
                if c not in rem:
                    s += c
            if s != '':
                npbyl[len(s)] = npbyl.get(len(s), []) + [ s ]


    pbyl = npbyl

    # il reste 3 et 4 à 2
    # ils ont d en commun
    for c in pbyl[2][0]:
        if c in pbyl[2][1]:
            cor[c] = 'd'
            break

    npbyl = {}
    for n in pbyl:
        rem = list(cor.keys())
        for p in pbyl[n]:
            s = ''
            for c in p:
                if c not in rem:
                    s += c
            if s != '':
                npbyl[len(s)] = npbyl.get(len(s), []) + [ s ]

    pbyl = npbyl

    # il en reste 1 dans 3 c'est g et un dans 4 c'est b
    # g est le seul à etre dans tous ceux qui sont à 2
    co1 = pbyl[1][0][0]
    co2 = pbyl[1][1][0]

    if all(co1 in p for p in pbyl[2]):
        cor[co1] = 'g'
        cor[co2] = 'b'
    else:
        cor[co2] = 'g'
        cor[co1] = 'b'


    npbyl = {}
    for n in pbyl:
        rem = list(cor.keys())
        for p in pbyl[n]:
            s = ''
            for c in p:
                if c not in rem:
                    s += c
            if s != '':
                npbyl[len(s)] = npbyl.get(len(s), []) + [ s ]

    pbyl = npbyl

    cor[pbyl[1][0]] = 'e'


    n = ''
    for tgt in tgts:
        s = list(cor[c] for c in tgt)
        s.sort()
        s = ''.join(s)
        idx = pwires.index(s)
        n += str(idx)
    #print(int(n), n)
    num += int(n)

ans = num
print(ans)

#aoc.submit(2, ans)
