"""Advent of Code 2021, jour 7.

Force brute : pour chaque position candidate entre 0 et le maximum, on
calcule la somme des coûts de déplacement et on garde le minimum. Le coût
d'un déplacement de d vaut d (partie 1) ou 1 + 2 + ... + d = d(d+1)/2
(partie 2).
"""


def cout_minimal(positions, cout):
    return min(sum(cout(abs(p - i)) for p in positions)
               for i in range(max(positions) + 1))


def partie1(positions):
    return cout_minimal(positions, lambda d: d)


def partie2(positions):
    return cout_minimal(positions, lambda d: d * (d + 1) // 2)


positions = list(map(int, open('input.txt').read().strip().split(',')))
print('Partie 1 :', partie1(positions))
print('Partie 2 :', partie2(positions))
