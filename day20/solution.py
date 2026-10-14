"""Advent of Code 2021, jour 20.

L'image est l'ensemble des cases allumées, et chaque pas ne recalcule que
la boîte englobante agrandie d'une case. Difficulté : si la règle allume
une case entourée de cases éteintes (alg[0] == '#'), tout le fond infini
s'allume un pas sur deux. On stocke alors, un pas sur deux, l'ensemble des
cases *éteintes* : le drapeau source_inversee dit comment lire l'image
courante, resultat_inversee comment écrire la suivante.
Partie 1 : 2 pas ; partie 2 : 50 pas.
"""
from itertools import product


def lire_entree(nom):
    lignes = open(nom).read().strip().split('\n')
    regle = lignes[0]
    image = set()
    for j, ligne in enumerate(lignes[2:]):
        for i, c in enumerate(ligne):
            if c == '#':
                image.add((i, j))
    return regle, image


def indice(image, i, j, inversee):
    """Entier codé par le voisinage 3 × 3 de (i, j)."""
    n = 0
    for nj in range(j - 1, j + 2):
        for ni in range(i - 1, i + 2):
            allumee = ((ni, nj) in image) != inversee
            n = 2 * n + allumee
    return n


def boite(image):
    xs = [i for i, _ in image]
    ys = [j for _, j in image]
    return min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1


def evolue(regle, image, source_inversee, resultat_inversee):
    nouvelle = set()
    imin, imax, jmin, jmax = boite(image)
    # caractère de la règle correspondant aux cases à stocker
    stocke = '.' if resultat_inversee else '#'
    for i, j in product(range(imin, imax + 1), range(jmin, jmax + 1)):
        if regle[indice(image, i, j, source_inversee)] == stocke:
            nouvelle.add((i, j))
    return nouvelle


def nb_allumees(regle, image, nb_pas):
    # pas pairs : image normale -> image inversée (si le fond clignote)
    # pas impairs : image inversée -> image normale
    clignote = regle[0] == '#'
    for k in range(nb_pas):
        if k % 2 == 0:
            image = evolue(regle, image, False, clignote)
        else:
            image = evolue(regle, image, clignote, False)
    # nb_pas est pair : l'image finale est stockée normalement
    return len(image)


def partie1(regle, image):
    return nb_allumees(regle, image, 2)


def partie2(regle, image):
    return nb_allumees(regle, image, 50)


regle, image = lire_entree('input.txt')
print('Partie 1 :', partie1(regle, image))
print('Partie 2 :', partie2(regle, image))
