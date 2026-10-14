"""Advent of Code 2021, jour 25.

La classe Grille réduit les coordonnées modulo la largeur et la hauteur,
ce qui réalise le tore. Un pas se fait en deux demi-pas synchrones : on
construit une nouvelle grille où se déplacent les '>' dont la case de
droite est libre dans l'ancienne grille, puis on fait de même pour les 'v'
vers le bas. On compte les pas jusqu'au premier qui ne change rien.
Le jour 25 n'a qu'une partie à programmer.
"""
from itertools import product


class Grille:
    def __init__(self, w, h, cases=None):
        if cases is not None:
            self.cases = cases
        else:
            self.cases = [['.'] * w for _ in range(h)]
        self.w = w
        self.h = h

    def __getitem__(self, c):
        x, y = c
        return self.cases[y % self.h][x % self.w]

    def __setitem__(self, c, v):
        x, y = c
        self.cases[y % self.h][x % self.w] = v

    def coords(self):
        return product(range(self.w), range(self.h))


def deplace(grille, cible, delta):
    """Déplace simultanément tous les pions cible dont la case suivante est libre."""
    nouvelle = Grille(grille.w, grille.h)
    for x, y in grille.coords():
        if grille[x, y] == cible and grille[delta(x, y)] == '.':
            nouvelle[delta(x, y)] = cible
        elif grille[x, y] != '.':
            nouvelle[x, y] = grille[x, y]
    return nouvelle


def droite(x, y):
    return (x + 1, y)


def bas(x, y):
    return (x, y + 1)


def partie1(grille):
    nb_pas = 0
    while True:
        nouvelle = deplace(deplace(grille, '>', droite), 'v', bas)
        nb_pas += 1
        if nouvelle.cases == grille.cases:
            return nb_pas
        grille = nouvelle


lignes = [list(ligne) for ligne in open('input.txt').read().strip().split('\n')]
print('Partie 1 :', partie1(Grille(len(lignes[0]), len(lignes), lignes)))
