
y = w1+6;
z = 26*y+z;
y = w2+11;
z = 26*z+y;
y = w3+5;
z = 26*y+z;

6
11
5
6
8
14
9
4
7
13
11
11
6
1

def next(z, w, xdec, wdec, zred=False):
    x = z % 26 + xdec
    if zred: z //= 26
    if x != w:
        z = 26 * z + w + wdec
    return z

z = 0
z = next(z, w1, 13, 6)
    z = next(z, w2, 11, 11)
        z = next(z, w3, 12, 5)
            z = next(z, w4, 10, 6)
                z = next(z, w5, 14, 8)
                z = next(z, w6, -1, 14, True)
                # il faut w6 = w5 + 7 
                # donc w5,w6 in [(2,9),(1,8)]

                z = next(z, w7, 14, 9)
                z = next(z, w8, -16, 4, True)
                # il faut w8 = w7 - 7
                # donc w7,w8 in [(9,2),(8,1)]

            z = next(z, w9, -8, 7, True)
            # il faut w9 = w4 - 2
            # donc w4,w9 in [(9,7),(8,6),(7,5),(6,4),(5,3),(4,2),(3,1)]

                z = next(z, w10, 12, 13)
                z = next(z, w11, -16, 11, True)
                # il faut w11 = w10 - 3
                # donc w10,w11 in [(9,6),(8,5),(7,4),(6,3),(5,2),(4,1)]

        z = next(z, w12, -13, 11, True)
        # il faut w12 = w3 - 8
        # donc w3,w12 in [(9,1)]

    z = next(z, w13, -6, 6, True)
    # il faut w13 = w2 + 5
    # donc w2,w13 in [(4,9),(3,8),(2,7),(1,6)]

z = next(z, w14, -6, 1, True)
# il faut w14 = w1
# donc w1,w14 = [(9,9),...,(1,1)]

# plus grand (gauche a chaque fois) : 94992992796199
# plus petit (droite a chaque fois) : 11931881141161



