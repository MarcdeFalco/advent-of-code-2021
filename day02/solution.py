"""Advent of Code 2021, jour 2.

Simulation directe : on applique chaque commande à l'état du sous-marin,
(position, profondeur) pour la partie 1, (position, profondeur, visée) pour
la partie 2, puis on affiche le produit position × profondeur.
"""


def lire_commandes(nom):
    commandes = []
    for ligne in open(nom):
        direction, quantite = ligne.split()
        commandes.append((direction, int(quantite)))
    return commandes


def partie1(commandes):
    position, profondeur = 0, 0
    for direction, quantite in commandes:
        if direction == 'forward':
            position += quantite
        if direction == 'up':
            profondeur -= quantite
        if direction == 'down':
            profondeur += quantite
    return position * profondeur


def partie2(commandes):
    # up/down ne changent plus que la visée, qui agit lors de forward
    position, profondeur, visee = 0, 0, 0
    for direction, quantite in commandes:
        if direction == 'forward':
            position += quantite
            profondeur += visee * quantite
        if direction == 'up':
            visee -= quantite
        if direction == 'down':
            visee += quantite
    return position * profondeur


commandes = lire_commandes('input.txt')
print('Partie 1 :', partie1(commandes))
print('Partie 2 :', partie2(commandes))
