from itertools import permutations, product, combinations, tee
from collections import defaultdict, Counter
import sys
sys.path.append("..")
from speedaoc import AOC

import numpy as np
from numpy.linalg import matrix_power

lines = open('input.txt').read().split('\n')[:-1]
mol, instr = lines[0], lines[2:]

subst = {}
atoms = list(set(mol))
for l in instr:
    pair, ins = l.split(' -> ')
    if ins not in atoms:
        atoms.append(ins)

atoms.sort()
natoms = len(atoms)

i_atoms = { a:i for i, a in enumerate(atoms) }
def idx(a,b):
    return i_atoms[a] * natoms + i_atoms[b]
m = np.zeros( natoms*natoms, dtype='int' )
for i in range(len(mol)-1):
    m[idx(*mol[i:i+2])] += 1

m_repl = np.zeros( (natoms*natoms,natoms*natoms), dtype='int' )
for l in instr:
    (a,b), c = l.split(' -> ')
    m_repl[idx(a,b),idx(a,c)] += 1
    m_repl[idx(a,b),idx(c,b)] += 1

m_repl = m_repl.transpose()

res = matrix_power(m_repl,40) @ m.transpose()

count = []
for a in atoms:
    c = 0
    for b in atoms:
        c += res[idx(a,b)] + res[idx(b,a)]
    if a in [ mol[0], mol[-1] ]:
        c += 1
    count.append(c // 2)
    
print(max(count)-min(count))


