"""Advent of Code 2021, jour 5.

Chaque segment est tracé point par point en incrémentant un compteur par
case (dictionnaire) ; on compte ensuite les cases couvertes au moins deux
fois. La partie 1 ne trace que les segments horizontaux et verticaux, la
partie 2 ajoute les diagonales (pente ±1).
"""


def lire_segments(nom):
    segments = []
    for ligne in open(nom).read().strip().split('\n'):
        a, b = ligne.split(' -> ')
        x1, y1 = map(int, a.split(','))
        x2, y2 = map(int, b.split(','))
        segments.append((x1, y1, x2, y2))
    return segments


def recouvrements(segments, avec_diagonales):
    compteurs = {}
    for x1, y1, x2, y2 in segments:
        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1
            for y in range(y1, y2 + 1):
                compteurs[x1, y] = compteurs.get((x1, y), 0) + 1
        elif y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1
            for x in range(x1, x2 + 1):
                compteurs[x, y1] = compteurs.get((x, y1), 0) + 1
        elif avec_diagonales:
            pente = (x2 - x1) / (y2 - y1)
            if pente in [1., -1.]:
                # on parcourt le segment de gauche à droite
                if x1 > x2:
                    x1, x2, y1, y2 = x2, x1, y2, y1
                for k in range(x2 - x1 + 1):
                    nx, ny = x1 + k, y1 + int(pente) * k
                    compteurs[nx, ny] = compteurs.get((nx, ny), 0) + 1

    return sum(1 for case in compteurs if compteurs[case] > 1)


def partie1(segments):
    return recouvrements(segments, False)


def partie2(segments):
    return recouvrements(segments, True)


segments = lire_segments('input.txt')
print('Partie 1 :', partie1(segments))
print('Partie 2 :', partie2(segments))
