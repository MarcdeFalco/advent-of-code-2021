"""Advent of Code 2021, jour 16.

Descente récursive sur un flux de bits : l'en-tête de chaque paquet dit
s'il s'agit d'un littéral ou d'un opérateur, et comment lire ses
sous-paquets (par longueur totale en bits ou par nombre). Chaque paquet lu
retient le nombre de bits qu'il occupe. On obtient un arbre d'expression :
partie 1, somme des versions ; partie 2, valeur de l'expression.
"""
from math import prod


class FluxBits:
    """Lecture bit à bit d'une chaîne hexadécimale."""

    def __init__(self, hexa):
        def bits(s):
            for c in s:
                yield from format(int(c, 16), '04b')

        self.gen = bits(hexa)

    def __call__(self, n):
        """Lit n bits et renvoie l'entier qu'ils codent."""
        return int(''.join(next(self.gen) for _ in range(n)), 2)

    def litteral(self):
        """Lit des groupes de 5 bits jusqu'à celui dont le premier bit est 0."""
        valeur = 0
        taille = 0
        while True:
            entete = self(1)
            valeur = 16 * valeur + self(4)
            taille += 5
            if entete == 0:
                return valeur, taille


class Paquet:
    def __init__(self, version, pid, taille, sous_paquets=None):
        self.version = version
        self.pid = pid
        self.taille = taille  # nombre de bits occupés par le paquet
        self.sous_paquets = [] if sous_paquets is None else sous_paquets

    def somme_versions(self):
        return self.version + sum(p.somme_versions() for p in self.sous_paquets)


class Litteral(Paquet):
    def __init__(self, version, pid, taille, valeur):
        super().__init__(version, pid, taille)
        self.valeur_litterale = valeur

    def valeur(self):
        return self.valeur_litterale


class Operateur(Paquet):
    OPERATIONS = {
        0: sum,
        1: prod,
        2: min,
        3: max,
        5: lambda v: 1 if v[0] > v[1] else 0,
        6: lambda v: 1 if v[0] < v[1] else 0,
        7: lambda v: 1 if v[0] == v[1] else 0,
    }

    def valeur(self):
        return self.OPERATIONS[self.pid]([p.valeur() for p in self.sous_paquets])


def lit_paquet(flux):
    version = flux(3)
    pid = flux(3)
    taille = 6
    if pid == 4:
        valeur, taille_valeur = flux.litteral()
        return Litteral(version, pid, taille + taille_valeur, valeur)

    type_longueur = flux(1)
    taille += 1
    sous_paquets = []
    if type_longueur == 0:
        # les sous-paquets occupent exactement longueur bits
        longueur = flux(15)
        taille += 15 + longueur
        while longueur > 0:
            p = lit_paquet(flux)
            sous_paquets.append(p)
            longueur -= p.taille
    else:
        # on connaît le nombre de sous-paquets
        nombre = flux(11)
        taille += 11
        for _ in range(nombre):
            p = lit_paquet(flux)
            sous_paquets.append(p)
            taille += p.taille
    return Operateur(version, pid, taille, sous_paquets)


def partie1(paquet):
    return paquet.somme_versions()


def partie2(paquet):
    return paquet.valeur()


paquet = lit_paquet(FluxBits(open('input.txt').read().strip()))
print('Partie 1 :', partie1(paquet))
print('Partie 2 :', partie2(paquet))
