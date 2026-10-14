"""Advent of Code 2021, jour 14.

On ne construit pas le mot, dont la longueur double à chaque pas : on suit
le vecteur v des effectifs des k^2 paires de lettres. Une règle ab -> c
envoie l'effectif de ab sur ac et cb, donc un pas est linéaire : v devient
M v, et après n pas on calcule M^n v avec matrix_power (exponentiation
rapide). Chaque lettre est comptée deux fois dans les paires, sauf les deux
extrémités du mot (qui ne changent jamais) : on les ajoute avant de diviser
par 2.
Si le mot commence et finit par la même lettre, elle est ajoutée deux fois.
"""
import numpy as np
from numpy.linalg import matrix_power


def lire_entree(nom):
    lignes = open(nom).read().strip().split('\n')
    mot = lignes[0]
    regles = [ligne.split(' -> ') for ligne in lignes[2:]]
    return mot, regles


def ecart(mot, regles, nb_pas):
    lettres = set(mot)
    for _, c in regles:
        lettres.add(c)
    lettres = sorted(lettres)
    k = len(lettres)
    indice = {a: i for i, a in enumerate(lettres)}

    def idx(a, b):
        """Indice de la paire ab dans le vecteur des effectifs."""
        return indice[a] * k + indice[b]

    v = np.zeros(k * k, dtype='int')
    for i in range(len(mot) - 1):
        v[idx(mot[i], mot[i + 1])] += 1

    # M[ac, ab] = M[cb, ab] = 1 pour chaque règle ab -> c
    M = np.zeros((k * k, k * k), dtype='int')
    for (a, b), c in regles:
        M[idx(a, c), idx(a, b)] += 1
        M[idx(c, b), idx(a, b)] += 1

    res = matrix_power(M, nb_pas) @ v

    effectifs = []
    for a in lettres:
        c = sum(res[idx(a, b)] + res[idx(b, a)] for b in lettres)
        c += (a == mot[0]) + (a == mot[-1])
        effectifs.append(c // 2)
    return max(effectifs) - min(effectifs)


def partie1(mot, regles):
    return ecart(mot, regles, 10)


def partie2(mot, regles):
    return ecart(mot, regles, 40)


mot, regles = lire_entree('input.txt')
print('Partie 1 :', partie1(mot, regles))
print('Partie 2 :', partie2(mot, regles))
