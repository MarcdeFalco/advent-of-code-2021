"""Advent of Code 2021, jour 12.

Retour sur trace : visit prolonge le chemin courant par chaque voisin
autorisé et somme les chemins obtenus jusqu'à 'end'. L'état est l'ensemble
des petites cavernes (en minuscules) déjà visitées et un booléen indiquant
si la seconde visite d'une petite caverne a déjà été utilisée ; la partie 1
est le cas où elle l'est dès le départ.
"""
from collections import defaultdict


def lire_graphe(nom):
    graphe = defaultdict(list)
    for ligne in open(nom).read().strip().split('\n'):
        a, b = ligne.split('-')
        graphe[a].append(b)
        graphe[b].append(a)
    return graphe


def visit(graphe, x, petites, double_utilise):
    """Nombre de chemins de x à 'end' ; petites : petites cavernes déjà vues."""
    nb_chemins = 0
    for v in graphe[x]:
        if v == 'start':
            continue
        if v == 'end':
            nb_chemins += 1
        elif v.islower():  # petite caverne
            if v in petites and not double_utilise:
                nb_chemins += visit(graphe, v, petites, True)
            elif v not in petites:
                # ensemble neuf : rien à annuler au retour
                nb_chemins += visit(graphe, v, petites | {v}, double_utilise)
        else:
            nb_chemins += visit(graphe, v, petites, double_utilise)
    return nb_chemins


def partie1(graphe):
    return visit(graphe, 'start', set(), True)


def partie2(graphe):
    return visit(graphe, 'start', set(), False)


graphe = lire_graphe('input.txt')
print('Partie 1 :', partie1(graphe))
print('Partie 2 :', partie2(graphe))
