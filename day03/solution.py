"""Advent of Code 2021, jour 3.

Partie 1 : pour chaque colonne, on compte les '1' ; le mot des bits
majoritaires donne un entier m, celui des bits minoritaires est son
complément 2^largeur - 1 - m.
Partie 2 : filtrage récursif, colonne par colonne, en ne gardant que les mots
qui ont le bit majoritaire (ou minoritaire) jusqu'à ce qu'il en reste un.
"""


def partie1(mots):
    largeur = len(mots[0])
    n = len(mots)
    majoritaires = ''
    for i in range(largeur):
        nb_uns = [mot[i] for mot in mots].count('1')
        majoritaires += '1' if nb_uns > n // 2 else '0'
    plus = int(majoritaires, 2)
    moins = 2 ** largeur - plus - 1
    return plus * moins


def recherche(mots, i, majoritaire=True):
    """Filtre les mots sur le bit i jusqu'à ce qu'il n'en reste qu'un."""
    if len(mots) == 1:
        return int(mots[0], 2)

    avec_1 = [mot for mot in mots if mot[i] == '1']
    avec_0 = [mot for mot in mots if mot[i] == '0']
    n1, n0 = len(avec_1), len(avec_0)
    # pour le critère minoritaire, on échange simplement les deux listes :
    # en cas d'égalité on garde alors les mots ayant un '0'
    if not majoritaire:
        avec_1, avec_0 = avec_0, avec_1

    if n1 >= n0:
        return recherche(avec_1, i + 1, majoritaire)
    else:
        return recherche(avec_0, i + 1, majoritaire)


def partie2(mots):
    oxygene = recherche(mots, 0, True)
    co2 = recherche(mots, 0, False)
    return oxygene * co2


mots = [ligne.strip() for ligne in open('input.txt')]
print('Partie 1 :', partie1(mots))
print('Partie 2 :', partie2(mots))
