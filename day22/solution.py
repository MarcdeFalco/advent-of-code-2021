"""Advent of Code 2021, jour 22.

On maintient une liste de pavés deux à deux disjoints, tous allumés. Pour
chaque instruction, on retire le nouveau pavé de chacun des pavés
existants : chaque axe est coupé en au plus trois intervalles, ce qui donne
au plus 27 sous-pavés, dont on garde ceux qui n'intersectent pas le
nouveau pavé. Si l'instruction allume, on ajoute ensuite le nouveau pavé.
Le nombre de cubes allumés est la somme des volumes.
Partie 1 : seulement les instructions contenues dans [-50, 50]^3.
Partie 2 : toutes les instructions.
"""
import re
from itertools import product


class Pave:
    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.x = (x1, x2)
        self.y = (y1, y2)
        self.z = (z1, z2)

    def intersecte(self, autre):
        def inter(a, b, c, d):
            return not (b < c or d < a)
        return (inter(*self.x, *autre.x) and inter(*self.y, *autre.y)
                and inter(*self.z, *autre.z))

    def contient(self, autre):
        def ct(a, b, c, d):
            return a <= c <= d <= b
        return (ct(*self.x, *autre.x) and ct(*self.y, *autre.y)
                and ct(*self.z, *autre.z))

    def retire(self, autre):
        """Liste de pavés disjoints dont l'union est self privé de autre."""
        if not self.intersecte(autre):
            return [self]

        def coupe(x1, x2, r1, r2):
            """Découpe [x1, x2] selon les bornes de [r1, r2]."""
            if r1 <= x1 <= x2 <= r2:
                return [(x1, x2)]
            if x1 < r1 <= r2 < x2:
                return [(x1, r1 - 1), (r1, r2), (r2 + 1, x2)]
            if x1 <= r2 < x2:
                return [(x1, r2), (r2 + 1, x2)]
            if x1 < r1 <= x2:
                return [(x1, r1 - 1), (r1, x2)]
            return [(x1, x2)]

        xs = coupe(*self.x, *autre.x)
        ys = coupe(*self.y, *autre.y)
        zs = coupe(*self.z, *autre.z)

        morceaux = []
        for (x1, x2), (y1, y2), (z1, z2) in product(xs, ys, zs):
            morceau = Pave(x1, x2, y1, y2, z1, z2)
            if not morceau.intersecte(autre):
                morceaux.append(morceau)
        return morceaux

    def volume(self):
        x1, x2 = self.x
        y1, y2 = self.y
        z1, z2 = self.z
        return (1 + x2 - x1) * (1 + y2 - y1) * (1 + z2 - z1)


def lire_instructions(nom):
    motif = re.compile(r'(on|off) x=(.*)\.\.(.*),y=(.*)\.\.(.*),z=(.*)\.\.(.*)')
    instructions = []
    for ligne in open(nom).read().strip().split('\n'):
        etat, *bornes = motif.match(ligne).groups()
        instructions.append((etat, Pave(*map(int, bornes))))
    return instructions


def applique(instructions):
    """Liste de pavés disjoints allumés après les instructions."""
    paves = []
    for etat, nouveau in instructions:
        paves = sum((pave.retire(nouveau) for pave in paves), [])
        if etat == 'on':
            paves.append(nouveau)
    return paves


def partie1(instructions):
    zone = Pave(-50, 50, -50, 50, -50, 50)
    paves = applique([(e, p) for e, p in instructions if zone.contient(p)])
    return sum(p.volume() for p in paves)


def partie2(instructions):
    return sum(p.volume() for p in applique(instructions))


if __name__ == '__main__':
    instructions = lire_instructions('input.txt')
    print('Partie 1 :', partie1(instructions))
    print('Partie 2 :', partie2(instructions))
