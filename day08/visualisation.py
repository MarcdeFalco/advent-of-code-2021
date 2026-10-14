"""Advent of Code 2021, jour 8 : graphe des intersections des dix chiffres.

Affiche au format Graphviz (dot) le graphe complet dont les sommets sont les
chiffres 0 à 9 et dont chaque arête porte le nombre de segments communs aux
deux chiffres. La somme des étiquettes autour d'un sommet est la signature
utilisée par solution_intersections.py.
Usage : python3 visualisation.py | dot -Tpng -o graphe.png
"""
from itertools import combinations

CHIFFRES = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf',
            'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']

print('graph G {')
for i, j in combinations(range(10), 2):
    communs = len(set(CHIFFRES[i]) & set(CHIFFRES[j]))
    print('%d -- %d [label=%d];' % (i, j, communs))
print('}')
