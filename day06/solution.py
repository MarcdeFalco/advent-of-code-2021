"""Advent of Code 2021, jour 6.

On ne simule pas chaque poisson (croissance exponentielle) : on garde
seulement l'histogramme des valeurs du compteur (9 cases). Un jour décale
l'histogramme d'une case ; les poissons à 0 repartent à 6 et créent autant
de nouveaux poissons à 8. Coût O(9) par jour.
"""


def population(poissons, nb_jours):
    effectifs = [0] * 9
    for p in poissons:
        effectifs[p] += 1

    for _ in range(nb_jours):
        nouveaux = [0] * 9
        for i in range(8):
            nouveaux[i] = effectifs[i + 1]
        nouveaux[8] += effectifs[0]
        nouveaux[6] += effectifs[0]
        effectifs = nouveaux

    return sum(effectifs)


def partie1(poissons):
    return population(poissons, 80)


def partie2(poissons):
    return population(poissons, 256)


poissons = list(map(int, open('input.txt').read().strip().split(',')))
print('Partie 1 :', partie1(poissons))
print('Partie 2 :', partie2(poissons))
