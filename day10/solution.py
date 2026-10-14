"""Advent of Code 2021, jour 10.

Pour chaque ligne, on empile la fermante attendue à chaque ouvrante et on
dépile à chaque fermante. Un désaccord donne le premier caractère fautif
(partie 1). Si la ligne se termine sans erreur, la pile restante, lue du
sommet vers le fond, est exactement la complétion (partie 2), dont le score
s'écrit en base 5. On garde le score médian.
"""

FERMANTE = {'(': ')', '[': ']', '{': '}', '<': '>'}
SCORE_ERREUR = {')': 3, ']': 57, '}': 1197, '>': 25137}


def verifie(ligne):
    """Renvoie (caractère fautif, None) ou (None, pile des fermantes attendues)."""
    pile = []
    for c in ligne:
        if c in FERMANTE:
            pile.append(FERMANTE[c])
        elif pile == [] or pile.pop() != c:
            return c, None
    return None, pile


def partie1(lignes):
    total = 0
    for ligne in lignes:
        fautif, _ = verifie(ligne)
        if fautif is not None:
            total += SCORE_ERREUR[fautif]
    return total


def partie2(lignes):
    scores = []
    for ligne in lignes:
        fautif, pile = verifie(ligne)
        if fautif is None:
            score = 0
            for c in reversed(pile):
                score = 5 * score + ')]}>'.index(c) + 1
            scores.append(score)
    scores.sort()
    return scores[len(scores) // 2]


lignes = [ligne.strip() for ligne in open('input.txt') if ligne.strip() != '']
print('Partie 1 :', partie1(lignes))
print('Partie 2 :', partie2(lignes))
