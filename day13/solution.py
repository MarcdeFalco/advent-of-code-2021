"""Advent of Code 2021, jour 13.

Les points sont les clés d'un dictionnaire. Un pliage selon y = n envoie
(x, y) sur (x, 2n - y) pour y > n (de même en x) ; les points superposés se
confondent naturellement dans le dictionnaire.
Partie 1 : nombre de points après le premier pliage.
Partie 2 : après tous les pliages, on affiche les points pour lire le code.
"""


def lire_entree(nom):
    points = set()
    pliages = []
    for ligne in open(nom).read().split('\n'):
        if ligne == '':
            continue
        if ligne.startswith('fold'):
            i = ligne.index('=')
            pliages.append((ligne[i - 1], int(ligne[i + 1:])))
        else:
            x, y = map(int, ligne.split(','))
            points.add((x, y))
    return points, pliages


def plie(points, direction, n):
    resultat = set()
    for x, y in points:
        if direction == 'y' and y > n:
            y = n - (y - n)
        if direction == 'x' and x > n:
            x = n - (x - n)
        resultat.add((x, y))
    return resultat


def partie1(points, pliages):
    direction, n = pliages[0]
    return len(plie(points, direction, n))


def partie2(points, pliages):
    for direction, n in pliages:
        points = plie(points, direction, n)
    largeur = max(x for x, _ in points) + 1
    hauteur = max(y for _, y in points) + 1
    return '\n'.join(''.join('#' if (x, y) in points else '.'
                             for x in range(largeur))
                     for y in range(hauteur))


points, pliages = lire_entree('input.txt')
print('Partie 1 :', partie1(points, pliages))
print('Partie 2 :')
print(partie2(points, pliages))
