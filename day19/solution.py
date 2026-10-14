"""Advent of Code 2021, jour 19.

On énumère les 24 rotations directes de l'espace comme permutations signées
des axes. Pour chaque scanner, chaque rotation et chaque balise, on
précalcule la liste des vecteurs allant de cette balise aux autres balises
du scanner. Deux balises de deux scanners coïncident si leurs listes ont au
moins 12 vecteurs communs ; la position relative du second scanner s'en
déduit. Un parcours depuis le scanner 0 recale de proche en proche tous les
scanners dans le repère du scanner 0.
Partie 1 : nombre de balises distinctes.
Partie 2 : plus grande distance de Manhattan entre deux scanners.
"""
from itertools import product


def lire_scanners(nom):
    lignes = open(nom).read().strip().split('\n')
    scanners = []
    i = 0
    while i < len(lignes):
        i += 1  # ligne '--- scanner n ---'
        scanner = []
        while i < len(lignes) and lignes[i] != '':
            scanner.append(tuple(map(int, lignes[i].split(','))))
            i += 1
        scanners.append(scanner)
        i += 1
    return scanners


# Les 24 orientations directes : ((axe, signe), (axe, signe), (axe, signe))
# donne, pour chaque nouvelle coordonnée, l'axe d'origine et le signe.
ORIENTATIONS = []
for x, sig in product(range(3), [1, -1]):
    y = (x + 1 * sig) % 3
    z = (x + 2 * sig) % 3
    ORIENTATIONS += [
        ((x, sig), (y, 1), (z, 1)),
        ((x, sig), (z, 1), (y, -1)),
        ((x, sig), (y, -1), (z, -1)),
        ((x, sig), (z, -1), (y, 1)),
    ]


def oriente_point(t, orientation):
    (a1, s1), (a2, s2), (a3, s3) = orientation
    return (s1 * t[a1], s2 * t[a2], s3 * t[a3])


def oriente(scanner, orientation):
    return [oriente_point(t, orientation) for t in scanner]


def diff(b, b1):
    return (b[0] - b1[0], b[1] - b1[1], b[2] - b1[2])


def add(b, b1):
    return (b[0] + b1[0], b[1] + b1[1], b[2] + b1[2])


def aligne(scanners):
    """Recale les scanners sur le scanner 0.

    Renvoie (scanners réorientés, positions, orientations), les deux
    derniers étant des dictionnaires indexés par le numéro du scanner.
    """
    scanners = scanners[:]
    nb = len(scanners)
    orientation = {0: ORIENTATIONS[0]}
    position = {0: (0, 0, 0)}

    # empreintes[s][o][i] : vecteurs de la balise i vers les autres balises
    # du scanner s, dans l'orientation o
    empreintes = []
    for s in scanners:
        par_orientation = {}
        for o in ORIENTATIONS:
            so = oriente(s, o)
            par_orientation[o] = [[diff(autre, b) for autre in so] for b in so]
        empreintes.append(par_orientation)

    a_visiter = [0]
    vus = set()
    while a_visiter != []:
        i1 = a_visiter.pop()
        if i1 in vus:
            continue
        vus.add(i1)
        sc1 = scanners[i1]  # déjà orienté comme le scanner 0
        o1 = orientation[i1]

        for i2 in range(nb):
            if i2 in position:
                continue
            for o2, (ib1, e1) in product(ORIENTATIONS, enumerate(empreintes[i1][o1])):
                trouve = False
                for ib2, e2 in enumerate(empreintes[i2][o2]):
                    if len(set(e1) & set(e2)) >= 12:
                        trouve = True
                        sc2 = oriente(scanners[i2], o2)
                        # les balises b1 et b2 coïncident : p2 + b2 = p1 + b1
                        position[i2] = diff(add(position[i1], sc1[ib1]), sc2[ib2])
                        orientation[i2] = o2
                        scanners[i2] = sc2
                        a_visiter.append(i2)
                        break
                if trouve:
                    break

    return scanners, position, orientation


def balises(scanners, position):
    return {add(b, position[i]) for i in range(len(scanners)) for b in scanners[i]}


def manhattan(p1, p2):
    return sum(abs(v1 - v2) for v1, v2 in zip(p1, p2))


def partie1(scanners, position):
    return len(balises(scanners, position))


def partie2(position):
    return max(manhattan(p1, p2) for p1, p2 in product(position.values(), repeat=2))


if __name__ == '__main__':
    scanners, position, _ = aligne(lire_scanners('input.txt'))
    print('Partie 1 :', partie1(scanners, position))
    print('Partie 2 :', partie2(position))
