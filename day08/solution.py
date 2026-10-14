"""Advent of Code 2021, jour 8.

Force brute : pour chaque ligne, on essaie les 7! = 5040 permutations des
segments et on garde la première qui transforme les dix motifs observés en
dix chiffres valides ; on décode ensuite les quatre chiffres affichés.
Partie 1 : nombre de chiffres affichés égaux à 1, 4, 7 ou 8.
Partie 2 : somme des nombres affichés.
"""
from itertools import permutations

# segments allumés pour chaque chiffre de 0 à 9
CHIFFRES = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf',
            'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']


def permute(motif, perm):
    """Image du motif par la permutation (lettre perm[i] -> i-ème lettre)."""
    return ''.join(sorted(chr(perm.index(c) + ord('a')) for c in motif))


def decode(motifs, affiches):
    """Liste des chiffres affichés, une fois la permutation retrouvée."""
    for perm in permutations('abcdefg'):
        if all(permute(m, perm) in CHIFFRES for m in motifs):
            break
    return [CHIFFRES.index(permute(a, perm)) for a in affiches]


def lire_entree(nom):
    lignes = []
    for ligne in open(nom):
        motifs, affiches = ligne.split(' | ')
        lignes.append((motifs.split(), affiches.split()))
    return lignes


def partie1(decodes):
    return sum(1 for chiffres in decodes for c in chiffres if c in (1, 4, 7, 8))


def partie2(decodes):
    return sum(int(''.join(map(str, chiffres))) for chiffres in decodes)


decodes = [decode(motifs, affiches) for motifs, affiches in lire_entree('input.txt')]
print('Partie 1 :', partie1(decodes))
print('Partie 2 :', partie2(decodes))
