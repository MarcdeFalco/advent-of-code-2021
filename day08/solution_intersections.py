"""Advent of Code 2021, jour 8 : variante sans recherche de permutation.

Chaque motif reçoit comme signature la somme des tailles de ses
intersections avec les neuf autres motifs de la ligne. Cette signature est
invariante par permutation des segments et différente pour les dix
chiffres : on identifie donc chaque motif en comparant sa signature à celle
des chiffres de référence. Les motifs sont codés en entiers (un bit par
segment) pour calculer les intersections avec &.
(visualisation.py dessine ce graphe d'intersections.)
"""
from itertools import combinations

CHIFFRES = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf',
            'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']


def nb_uns(n):
    return bin(n).count('1')


def en_entier(motif):
    return sum(1 << (ord(c) - ord('a')) for c in motif)


def signatures(motifs):
    """Pour chaque motif, somme des tailles des intersections avec les autres."""
    codes = [en_entier(m) for m in motifs]
    inter = {}
    for n1, n2 in combinations(codes, 2):
        inter[n1, n2] = inter[n2, n1] = nb_uns(n1 & n2)
    return [sum(inter[n, m] for m in codes if m != n) for n in codes]


SIGNATURES_REF = signatures(CHIFFRES)


def decode(motifs, affiches):
    motifs = [''.join(sorted(m)) for m in motifs]
    sig = signatures(motifs)
    return [SIGNATURES_REF.index(sig[motifs.index(''.join(sorted(a)))])
            for a in affiches]


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
