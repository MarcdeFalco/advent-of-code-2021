"""Advent of Code 2021, jour 22 : rendu POV-Ray du découpage en pavés.

Après chaque instruction, écrit un fichier cuboid_NNNN.pov décrivant la
liste courante de pavés disjoints (une boîte blanche par pavé). Les images
obtenues avec POV-Ray peuvent ensuite être assemblées en une animation.
"""
from solution import lire_instructions

ENTETE = '''camera { location <-200000,0,-200000>
  right image_width/image_height*x
  look_at <0,0,0> }

#default { finish { ambient 0 } }

light_source { <0,0,-200000> color<0.8,1,1> }
light_source { <-200000,0,0> color<1,0.8,1> }
light_source { <-200000,0,-200000> color<1,1,1> }

'''


def boite(pave):
    (x1, x2), (y1, y2), (z1, z2) = pave.x, pave.y, pave.z
    return ('box { <%f,%f,%f>, <%f,%f,%f> pigment { color<1,1,1> } }\n'
            % (x1 - 0.5, y1 - 0.5, z1 - 0.5, x2 + 0.5, y2 + 0.5, z2 + 0.5))


paves = []
for i, (etat, nouveau) in enumerate(lire_instructions('input.txt')):
    paves = sum((pave.retire(nouveau) for pave in paves), [])
    if etat == 'on':
        paves.append(nouveau)
    with open('cuboid_%04d.pov' % i, 'w') as f:
        f.write(ENTETE)
        for pave in paves:
            f.write(boite(pave))
