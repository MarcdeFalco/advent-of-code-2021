"""Advent of Code 2021, jour 21 (partie 2 seulement).

Les 27 issues de trois lancers du dé à trois faces sont regroupées par
somme avec leur multiplicité (7 sommes possibles). La fonction parties
renvoie le nombre d'univers gagnés par chaque joueur depuis un état
(joueur dont c'est le tour, scores, positions) et est mémoïsée : au plus
2 × 21² × 10² états.
Partie 1 : pas de solution.
"""
from itertools import product
from collections import Counter

# somme de trois lancers -> nombre de façons de l'obtenir
SOMMES = Counter(map(sum, product(range(1, 4), repeat=3)))

cache = {}


def parties(joueur, scores, positions):
    cle = (joueur, scores, positions)
    if cle in cache:
        return cache[cle]
    if scores[0] >= 21:
        return (1, 0)
    if scores[1] >= 21:
        return (0, 1)

    victoires = [0, 0]
    for somme, multiplicite in SOMMES.items():
        npos = list(positions)
        nscores = list(scores)
        npos[joueur] = 1 + (positions[joueur] + somme - 1) % 10
        nscores[joueur] += npos[joueur]
        v = parties(1 - joueur, tuple(nscores), tuple(npos))
        victoires[0] += multiplicite * v[0]
        victoires[1] += multiplicite * v[1]
    cache[cle] = tuple(victoires)
    return cache[cle]


def partie2(positions):
    return max(parties(0, (0, 0), tuple(positions)))


positions = [int(ligne.split(': ')[1]) for ligne in open('input.txt').read().strip().split('\n')]
print('Partie 2 :', partie2(positions))
