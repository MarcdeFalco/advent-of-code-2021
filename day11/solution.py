"""Advent of Code 2021, jour 11.

Simulation pas à pas. On incrémente toutes les cases, puis on traite une
pile de cases à faire flasher : chaque flash incrémente les huit voisins,
qui peuvent rejoindre la pile. Un état par case (NON, A_FLASHER, A_FLASHE)
garantit qu'une case flashe au plus une fois par pas.
Partie 1 : nombre de flashs en 100 pas.
Partie 2 : premier pas où toutes les cases flashent ensemble.
"""
from itertools import product
from collections import defaultdict

NON, A_FLASHER, A_FLASHE = 0, 1, 2


def voisins(x, y, w, h):
    for dx, dy in product(range(-1, 2), repeat=2):
        if (dx, dy) != (0, 0):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                yield nx, ny


def pas(m):
    """Effectue un pas sur la grille m (modifiée) ; renvoie le nombre de flashs."""
    w, h = len(m), len(m[0])
    etat = defaultdict(int)
    a_flasher = []
    for x, y in product(range(w), range(h)):
        m[x][y] += 1
        if m[x][y] > 9:
            a_flasher.append((x, y))
            etat[x, y] = A_FLASHER

    while a_flasher != []:
        x, y = a_flasher.pop()
        etat[x, y] = A_FLASHE
        for nx, ny in voisins(x, y, w, h):
            m[nx][ny] += 1
            if m[nx][ny] > 9 and etat[nx, ny] == NON:
                a_flasher.append((nx, ny))
                etat[nx, ny] = A_FLASHER

    # seules les cases qui ont flashé figurent dans etat : on les remet à 0
    for x, y in etat:
        m[x][y] = 0
    return len(etat)


def partie1(grille):
    m = [ligne[:] for ligne in grille]
    return sum(pas(m) for _ in range(100))


def partie2(grille):
    m = [ligne[:] for ligne in grille]
    nb_cases = len(m) * len(m[0])
    n = 1
    while pas(m) != nb_cases:
        n += 1
    return n


grille = [[int(c) for c in ligne.strip()] for ligne in open('input.txt') if ligne.strip() != '']
print('Partie 1 :', partie1(grille))
print('Partie 2 :', partie2(grille))
