"""Advent of Code 2021, jour 14 : graphe de transition des paires.

Affiche au format Graphviz (dot) le graphe orienté dont les sommets sont
les paires de lettres et où chaque règle ab -> c donne les arcs ab -> ac et
ab -> cb : c'est le graphe de la matrice M utilisée par solution.py.
Usage : python3 visualisation.py | dot -Tpng -o graphe.png
"""
lignes = open('input.txt').read().strip().split('\n')
print('digraph G {')
for ligne in lignes[2:]:
    (a, b), c = ligne.split(' -> ')
    print('%s%s -> %s%s;' % (a, b, a, c))
    print('%s%s -> %s%s;' % (a, b, c, b))
print('}')
