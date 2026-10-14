"""Advent of Code 2021, jour 19 : dessin TikZ des scanners recalés.

Pour chaque scanner : son cube de portée (pointillés), des traits vers les
balises qu'il voit, deux flèches donnant son orientation, et son numéro ;
les balises sont des points rouges. La sortie est à inclure dans un
document LaTeX chargeant TikZ.
Usage : python3 visualisation.py > dessin.tikz
"""
from itertools import product

from solution import lire_scanners, aligne, balises, add

PORTEE = 1000
COULEURS = ['green', 'blue', 'cyan', 'magenta', 'yellow', 'gray', 'darkgray',
            'lightgray', 'brown', 'lime', 'olive', 'orange', 'pink', 'purple',
            'teal', 'violet'] * 3


def echelle(x, y, z):
    s = 0.005
    return (x * s, y * s, z * s)


def norme_infinie(p1, p2):
    return max(abs(v1 - v2) for v1, v2 in zip(p1, p2))


def trait(style, p1, p2):
    print('\\draw[%s] (%0.2f,%0.2f,%0.2f) -- (%0.2f,%0.2f,%0.2f);'
          % ((style,) + echelle(*p1) + echelle(*p2)))


def fleche(axe, signe):
    v = [0, 0, 0]
    v[axe] = signe * PORTEE / 3
    return tuple(v)


scanners, position, orientation = aligne(lire_scanners('input.txt'))
toutes = balises(scanners, position)
w = PORTEE

print('\\begin{tikzpicture}')
for i in range(len(scanners)):
    p = position[i]
    for b in toutes:
        if norme_infinie(b, p) <= w:
            trait('very thin,' + COULEURS[i], p, b)

    # les 12 arêtes du cube de portée : deux coordonnées fixées à ±w,
    # la troisième variant de -w à w
    x, y, z = p
    for axe in range(3):
        for s1, s2 in product([-w, w], repeat=2):
            debut, fin = [0, 0, 0], [0, 0, 0]
            autres = [a for a in range(3) if a != axe]
            debut[autres[0]] = fin[autres[0]] = s1
            debut[autres[1]] = fin[autres[1]] = s2
            debut[axe], fin[axe] = -w, w
            trait('dotted,' + COULEURS[i], add(p, debut), add(p, fin))

    (a1, sg1), (a2, sg2), _ = orientation[i]
    trait('->', p, add(p, fleche(a1, sg1)))
    trait('dashed,->', p, add(p, fleche(a2, sg2)))
    print('\\node[circle,%s,text=black,fill,inner sep=1pt] '
          'at (%0.2f,%0.2f,%0.2f) {\\Large$S_{%d}$};'
          % ((COULEURS[i],) + echelle(*p) + (i,)))

for b in toutes:
    print('\\fill[red] (%0.2f,%0.2f,%0.2f) circle (2pt);' % echelle(*b))
print('\\end{tikzpicture}')
