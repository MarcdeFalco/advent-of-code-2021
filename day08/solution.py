from itertools import permutations

def permutes(s, perm):
    perm = list(perm)
    p = []
    for c in s:
        p.append(chr(perm.index(c) + ord('a')))
    p.sort()
    return ''.join(p)

answer = 0

for l in open('input.txt'):
    if l == '': break

    patterns = l.split(' | ')[0].split()
    tgts = l.split(' | ')[1].split()

    digits = [ 'abcefg', 'cf', 'acdeg', 'acdfg',
            'bcdf', 'abdfg', 'abdefg', 'acf',
            'abcdefg', 'abcdfg']

    for perm in permutations('abcdefg'):
        if all(permutes(p, perm) in digits for p in patterns):
            break

    num = int(''.join(str(digits.index(permutes(tgt, perm))) for tgt in tgts))
    answer += num

print('Part 2', answer)


