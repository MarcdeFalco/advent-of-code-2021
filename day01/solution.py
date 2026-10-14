"""Advent of Code 2021, jour 1.

Partie 1 : on compte les mesures plus grandes que la précédente.
Partie 2 : même chose sur la somme d'une fenêtre glissante de trois mesures,
mise à jour en retirant la plus ancienne valeur et en ajoutant la nouvelle.
"""


def partie1(profondeurs):
    augmentations = 0
    for i in range(1, len(profondeurs)):
        if profondeurs[i] > profondeurs[i - 1]:
            augmentations += 1
    return augmentations


def partie2(profondeurs):
    augmentations = 0
    fenetre = profondeurs[0] + profondeurs[1] + profondeurs[2]
    for i in range(3, len(profondeurs)):
        nouvelle_fenetre = fenetre - profondeurs[i - 3] + profondeurs[i]
        if nouvelle_fenetre > fenetre:
            augmentations += 1
        fenetre = nouvelle_fenetre
    return augmentations


profondeurs = [int(ligne) for ligne in open('input.txt')]
print('Partie 1 :', partie1(profondeurs))
print('Partie 2 :', partie2(profondeurs))
