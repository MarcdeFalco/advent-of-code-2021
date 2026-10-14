"""Advent of Code 2021, jour 14 : première version, sans matrice.

Partie 1 : 10 pas de réécriture effectués naïvement sur le mot.
Partie 2 : on ne garde qu'un dictionnaire paire -> effectif ; chaque règle
ab -> c envoie l'effectif de ab sur ac et cb. Chaque lettre est comptée
deux fois dans les paires sauf les extrémités du mot, d'où la correction
avant la division par 2.
On compte chaque lettre exactement : (max - min) // 2 + 1 ne compterait
pas correctement les extrémités en général.
"""
from collections import defaultdict, Counter


def lire_entree(nom):
    lignes = open(nom).read().strip().split('\n')
    mot = lignes[0]
    regles = dict(ligne.split(' -> ') for ligne in lignes[2:])
    return mot, regles


def remplace(mot, regles):
    sortie = ''
    for i in range(len(mot) - 1):
        sortie += mot[i]
        if mot[i:i + 2] in regles:
            sortie += regles[mot[i:i + 2]]
    return sortie + mot[-1]


def partie1(mot, regles):
    for _ in range(10):
        mot = remplace(mot, regles)
    effectifs = Counter(mot).most_common()
    return effectifs[0][1] - effectifs[-1][1]


def pas(paires, regles):
    nouvelles = defaultdict(int)
    for paire, n in paires.items():
        if paire in regles:
            nouvelles[paire[0] + regles[paire]] += n
            nouvelles[regles[paire] + paire[1]] += n
        else:
            nouvelles[paire] += n
    return nouvelles


def partie2(mot, regles):
    paires = defaultdict(int)
    for i in range(len(mot) - 1):
        paires[mot[i:i + 2]] += 1
    for _ in range(40):
        paires = pas(paires, regles)

    doubles = Counter()
    for paire, n in paires.items():
        doubles[paire[0]] += n
        doubles[paire[1]] += n
    doubles[mot[0]] += 1
    doubles[mot[-1]] += 1
    effectifs = [c // 2 for c in doubles.values()]
    return max(effectifs) - min(effectifs)


mot, regles = lire_entree('input.txt')
print('Partie 1 :', partie1(mot, regles))
print('Partie 2 :', partie2(mot, regles))
