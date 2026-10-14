"""Advent of Code 2021, jour 23.

Algorithme de Dijkstra sur l'espace des configurations, chaque
configuration étant la grille aplatie en chaîne. On ne génère que les coups
utiles : d'une chambre vers une case libre du couloir (hors entrées des
chambres), ou du couloir directement au fond de la chambre cible quand
celle-ci ne contient que des pions de la bonne couleur. La profondeur des
chambres est lue sur la grille, ce qui couvre les deux parties ; pour la
partie 2, on insère les deux lignes données par l'énoncé.
L'égalité entre configurations compare les grilles (et non les coûts),
pour ne pas redévelopper des configurations déjà traitées.
"""
from queue import PriorityQueue

LIGNES_PARTIE2 = ['  #D#C#B#A#  ', '  #D#B#A#C#  ']
W = 13  # largeur de la grille


class Coup:
    def __init__(self, couleur, src, dst):
        self.couleur = couleur
        self.src = src
        self.dst = dst

    def cout(self):
        # on passe toujours par le couloir : distance de Manhattan
        dx = abs(self.dst[0] - self.src[0])
        dy = abs(self.dst[1] - self.src[1])
        return 10 ** 'ABCD'.index(self.couleur) * (dx + dy)


class Configuration:
    def __init__(self, grille, h, cout=0):
        self.grille = grille  # chaîne de W * h caractères
        self.h = h
        self.cout = cout

    def __getitem__(self, case):
        x, y = case
        return self.grille[y * W + x]

    # ordre de la file de priorité : le coût
    def __lt__(self, autre):
        return self.cout < autre.cout

    # égalité (pour l'ensemble des configurations traitées) : la grille
    def __eq__(self, autre):
        return self.grille == autre.grille

    def __hash__(self):
        return hash(self.grille)

    def coups_depuis(self, x, y):
        c = self[x, y]
        h = self.h
        x_cible = 3 + 2 * 'ABCD'.index(c)

        if y == 1:  # dans le couloir : on ne peut qu'aller dans sa chambre
            chemin = range(x_cible, x) if x_cible < x else range(x + 1, x_cible)
            if all(self[tx, y] == '.' for tx in chemin):
                if all(self[x_cible, ty] in [c, '.'] for ty in range(2, h - 1)):
                    fond = max(ty for ty in range(2, h - 1) if self[x_cible, ty] == '.')
                    return [Coup(c, (x, y), (x_cible, fond))]
        elif all(self[x, ty] == '.' for ty in range(2, y)):
            # dans une chambre, sans pion au-dessus : on sort, sauf si le pion
            # est déjà dans sa chambre au-dessus de pions de sa couleur
            if x != x_cible or not all(self[x, ty] == c for ty in range(y + 1, h - 1)):
                libres = []
                xg = x - 1
                while self[xg, 1] == '.':
                    libres.append(xg)
                    xg -= 1
                xd = x + 1
                while self[xd, 1] == '.':
                    libres.append(xd)
                    xd += 1
                return [Coup(c, (x, y), (tx, 1))
                        for tx in libres if tx not in [3, 5, 7, 9]]

        return []

    def coups(self):
        return sum((self.coups_depuis(i % W, i // W)
                    for i, c in enumerate(self.grille) if c in 'ABCD'), [])

    def joue(self, coup):
        isrc = W * coup.src[1] + coup.src[0]
        idst = W * coup.dst[1] + coup.dst[0]
        c = self.grille[isrc]
        g = list(self.grille)
        g[isrc], g[idst] = '.', c
        return Configuration(''.join(g), self.h, self.cout + coup.cout())


def cout_minimal(lignes):
    h = len(lignes)
    rangee = '  #A#B#C#D#  '
    finale = '#############' + '#...........#' + '###A#B#C#D###' \
        + rangee * (h - 4) + '  #########  '

    a_visiter = PriorityQueue()
    a_visiter.put(Configuration(''.join(lignes), h))
    traitees = set()
    meilleur = float('inf')
    while not a_visiter.empty():
        conf = a_visiter.get()
        if conf.cout > meilleur or conf in traitees:
            continue
        traitees.add(conf)
        if conf.grille == finale:
            meilleur = min(meilleur, conf.cout)
        else:
            for coup in conf.coups():
                a_visiter.put(conf.joue(coup))
    return meilleur


def partie1(lignes):
    return cout_minimal(lignes)


def partie2(lignes):
    return cout_minimal(lignes[:3] + LIGNES_PARTIE2 + lignes[3:])


# on complète les lignes à la largeur W (espaces finaux parfois absents)
lignes = [ligne.ljust(W) for ligne in open('input.txt').read().rstrip('\n').split('\n')]
print('Partie 1 :', partie1(lignes))
print('Partie 2 :', partie2(lignes))
