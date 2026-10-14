"""Advent of Code 2021, jour 15.

Plus court chemin pondéré du coin haut gauche au coin bas droit :
algorithme de Dijkstra avec une file de priorité (PriorityQueue), où l'on
réinsère une case quand sa distance diminue au lieu de diminuer sa clé.
La partie 2 construit la grille 5 × 5 fois plus grande par deux
duplications, chaque copie ayant ses risques incrémentés (9 repasse à 1).
"""
from queue import PriorityQueue


def voisins(x, y, w, h):
    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h:
            yield nx, ny


def risque_minimal(risque):
    w, h = len(risque[0]), len(risque)
    a_visiter = PriorityQueue()
    total = [[float('inf')] * w for _ in range(h)]
    visite = [[False] * w for _ in range(h)]
    a_visiter.put((0, (0, 0)))
    total[0][0] = 0

    while not a_visiter.empty():
        # une case peut être extraite plusieurs fois : la relaxation lit
        # total[y][x], qui est déjà définitif, donc cela ne fausse rien
        _, (x, y) = a_visiter.get()
        visite[y][x] = True

        for vx, vy in voisins(x, y, w, h):
            if not visite[vy][vx]:
                nouveau = total[y][x] + risque[vy][vx]
                if nouveau < total[vy][vx]:
                    a_visiter.put((nouveau, (vx, vy)))
                    total[vy][vx] = nouveau

    return total[h - 1][w - 1]


def incremente(ligne, k):
    """Ajoute k à chaque risque, les valeurs au-delà de 9 repartant à 1."""
    return [c + k - 9 if c + k > 9 else c + k for c in ligne]


def agrandit(risque):
    """Grille 5 × 5 fois plus grande : en largeur, puis en hauteur."""
    lignes_larges = [sum((incremente(ligne, k) for k in range(5)), [])
                     for ligne in risque]
    return sum(([incremente(ligne, k) for ligne in lignes_larges]
                for k in range(5)), [])


def partie1(risque):
    return risque_minimal(risque)


def partie2(risque):
    return risque_minimal(agrandit(risque))


risque = [[int(c) for c in ligne.strip()] for ligne in open('input.txt')]
print('Partie 1 :', partie1(risque))
print('Partie 2 :', partie2(risque))
