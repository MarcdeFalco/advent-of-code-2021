"""Advent of Code 2021, jour 17.

Force brute : on simule toutes les vitesses initiales (vx, vy) avec
0 <= vx <= xmax et ymin <= vy < -ymin. Au-delà, la sonde dépasse la cible
dès le premier pas, ou bien, en redescendant, elle repasse par y = 0 avec
une vitesse -vy - 1 < ymin et saute la cible en un seul pas.
Partie 1 : hauteur maximale atteinte par une trajectoire qui touche la cible.
Partie 2 : nombre de vitesses initiales qui touchent la cible.
"""
import re


def lire_cible(nom):
    motif = re.compile(r'target area: x=(.*)\.\.(.*), y=(.*)\.\.(.*)')
    return tuple(map(int, motif.match(open(nom).read()).groups()))


def simule(cible):
    """Renvoie (hauteur maximale, ensemble des vitesses qui touchent)."""
    xmin, xmax, ymin, ymax = cible
    meilleure_hauteur = 0
    touchent = set()
    for vx0 in range(xmax + 1):
        for vy0 in range(ymin, -ymin):
            vx, vy = vx0, vy0
            x, y = 0, 0
            hauteur = 0
            while y >= ymin:
                x += vx
                y += vy
                hauteur = max(hauteur, y)
                if vx > 0:
                    vx -= 1
                vy -= 1
                if xmin <= x <= xmax and ymin <= y <= ymax:
                    meilleure_hauteur = max(meilleure_hauteur, hauteur)
                    touchent.add((vx0, vy0))
    return meilleure_hauteur, touchent


def partie1(cible):
    return simule(cible)[0]


def partie2(cible):
    return len(simule(cible)[1])


cible = lire_cible('input.txt')
print('Partie 1 :', partie1(cible))
print('Partie 2 :', partie2(cible))
