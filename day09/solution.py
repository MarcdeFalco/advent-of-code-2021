"""Advent of Code 2021, jour 9.

Partie 1 : un point bas est une case strictement plus basse que ses quatre
voisins ; on somme 1 + hauteur sur ces points.
Partie 2 : depuis chaque point bas, parcours en profondeur itératif (pile
tovisit) des cases de hauteur différente de 9 ; on multiplie les tailles
des trois plus grands bassins.
"""


def voisins(x, y, w, h):
    for vx, vy in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        if 0 <= vx < w and 0 <= vy < h:
            yield vx, vy


def points_bas(grille):
    w, h = len(grille[0]), len(grille)
    bas = []
    for x in range(w):
        for y in range(h):
            if min(grille[vy][vx] for vx, vy in voisins(x, y, w, h)) > grille[y][x]:
                bas.append((x, y))
    return bas


def partie1(grille):
    return sum(1 + grille[y][x] for x, y in points_bas(grille))


def partie2(grille):
    w, h = len(grille[0]), len(grille)
    tailles = []
    for x, y in points_bas(grille):
        bassin = []
        tovisit = [(x, y)]
        while tovisit != []:
            x, y = tovisit.pop()
            bassin.append((x, y))
            for vx, vy in voisins(x, y, w, h):
                # bassin et tovisit sont des listes : tests d'appartenance
                # linéaires, suffisants pour des bassins de cette taille
                if grille[vy][vx] != 9 and (vx, vy) not in bassin \
                        and (vx, vy) not in tovisit:
                    tovisit.append((vx, vy))
        tailles.append(len(bassin))

    tailles.sort()
    a, b, c = tailles[-3:]
    return a * b * c


grille = [[int(c) for c in ligne.strip()] for ligne in open('input.txt')]
print('Partie 1 :', partie1(grille))
print('Partie 2 :', partie2(grille))
