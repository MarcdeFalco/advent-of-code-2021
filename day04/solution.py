"""Advent of Code 2021, jour 4.

Simulation du bingo : les numéros tirés sont rayés en place (remplacés par
None) et, après chaque rayure, on teste les lignes et colonnes de la grille.
On note l'ordre dans lequel les grilles gagnent : la première donne la
partie 1, la dernière la partie 2.
"""


def lire_entree(nom):
    lignes = [ligne.strip() for ligne in open(nom)]
    numeros = list(map(int, lignes[0].split(',')))
    grilles = []
    i = 2
    while i < len(lignes):
        grille = []
        while i < len(lignes) and lignes[i] != '':
            grille.append(list(map(int, lignes[i].split())))
            i += 1
        i += 1
        grilles.append(grille)
    return numeros, grilles


def gagnante(grille):
    return any(all(grille[i][j] is None for j in range(5))
               or all(grille[j][i] is None for j in range(5))
               for i in range(5))


def score(grille, dernier_numero):
    somme = sum(sum(k for k in ligne if k is not None) for ligne in grille)
    return somme * dernier_numero


def jouer(numeros, grilles):
    """Renvoie la liste des (grille, numéro gagnant) dans l'ordre de victoire.

    Les grilles sont modifiées en place.
    """
    deja_gagnee = [False] * len(grilles)
    ordre = []
    for n in numeros:
        for k, grille in enumerate(grilles):
            if deja_gagnee[k]:
                continue
            for ligne in grille:
                if n in ligne:
                    ligne[ligne.index(n)] = None  # on raye n
                    if gagnante(grille):
                        deja_gagnee[k] = True
                        ordre.append((grille, n))
    return ordre


def partie1(ordre):
    grille, n = ordre[0]
    return score(grille, n)


def partie2(ordre):
    grille, n = ordre[-1]
    return score(grille, n)


numeros, grilles = lire_entree('input.txt')
ordre = jouer(numeros, grilles)
print('Partie 1 :', partie1(ordre))
print('Partie 2 :', partie2(ordre))
