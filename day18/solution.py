"""Advent of Code 2021, jour 18.

On travaille directement sur la chaîne de caractères. reduce_explode
parcourt les caractères en suivant la profondeur des crochets et repère la
première paire de deux nombres à profondeur > 4 ; add_left / add_right
ajoutent une valeur au premier nombre à gauche / à droite par manipulation
de sous-chaînes. reduce_split coupe le premier nombre >= 10. La magnitude
est calculée à la fin, après conversion de la chaîne en listes Python.
Partie 2 : on essaie tous les couples dans les deux ordres.
"""
import ast


def lit_nombre(s, i):
    """Lit l'entier qui commence en s[i] ; renvoie (valeur, indice du dernier chiffre)."""
    n = s[i]
    while i < len(s) - 1 and s[i + 1].isdigit():
        i += 1
        n += s[i]
    return int(n), i


def add_left(s, a):
    """Ajoute a au nombre le plus à droite de s."""
    i = len(s) - 1
    while i >= 0:
        if s[i].isdigit():
            fin = i
            while i > 0 and s[i - 1].isdigit():
                i -= 1
            return s[:i] + str(int(s[i:fin + 1]) + a) + s[fin + 1:]
        i -= 1
    return s


def add_right(s, a):
    """Ajoute a au nombre le plus à gauche de s."""
    i = 0
    while i < len(s):
        if s[i].isdigit():
            n, fin = lit_nombre(s, i)
            return s[:i] + str(n + a) + s[fin + 1:]
        i += 1
    return s


def explode(s, i, j, n1, n2):
    """La paire [n1,n2] occupe s[i-1:j+1] (crochets compris)."""
    return add_left(s[:i - 1], n1) + '0' + add_right(s[j + 1:], n2)


def reduce_explode(s):
    profondeur = 0
    premier = None  # (indice, valeur) du premier nombre de la paire courante
    i = 0
    while i < len(s):
        c = s[i]
        if c == '[':
            profondeur += 1
            premier = None
        elif c == ']':
            profondeur -= 1
            premier = None
        elif c == ',':
            pass
        elif premier is None:
            debut = i
            n, i = lit_nombre(s, i)
            premier = debut, n
        else:
            n2, i = lit_nombre(s, i)
            debut, n1 = premier
            if profondeur > 4:
                return explode(s, debut, i + 1, n1, n2)
        i += 1
    return s


def reduce_split(s):
    i = 0
    while i < len(s):
        if s[i].isdigit():
            debut = i
            n, i = lit_nombre(s, i)
            if n >= 10:
                a, b = n // 2, n - n // 2
                return s[:debut] + '[' + str(a) + ',' + str(b) + ']' + s[i + 1:]
        i += 1
    return s


def reduce(s):
    """Applique explode, sinon split, jusqu'à ce que rien ne change."""
    while True:
        r = reduce_explode(s)
        if r == s:
            r = reduce_split(s)
        if r == s:
            return s
        s = r


def add(s1, s2):
    return reduce('[' + s1 + ',' + s2 + ']')


def magnitude(nombre):
    if type(nombre) == int:
        return nombre
    a, b = nombre
    return 3 * magnitude(a) + 2 * magnitude(b)


def partie1(nombres):
    s = nombres[0]
    for autre in nombres[1:]:
        s = add(s, autre)
    return magnitude(ast.literal_eval(s))


def partie2(nombres):
    meilleure = 0
    for i1 in range(len(nombres)):
        for i2 in range(i1 + 1, len(nombres)):
            s1, s2 = nombres[i1], nombres[i2]
            for _ in range(2):
                meilleure = max(meilleure, magnitude(ast.literal_eval(add(s1, s2))))
                s1, s2 = s2, s1
    return meilleure


nombres = open('input.txt').read().strip().split('\n')
print('Partie 1 :', partie1(nombres))
print('Partie 2 :', partie2(nombres))
