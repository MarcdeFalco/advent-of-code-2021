import sys

def word(stack):
    s = ''
    for c in stack:
        s += chr(ord('a')+c)
    return s

constants = [ (13,6), (11,11), (12,5), (10,6), (14,8), (-1,14), (14,9),
        (-16,4), (-8,7), (12,13), (-16,11), (-13,11), (-6,6), (-6,1) ]

def simulate(ws):
    stack = []
    for w, c in zip(ws, constants):
        a, b = c
        top = stack[-1] if len(stack) > 0 else 0
        if a < 0:
            stack.pop()
        if top + a != w:
            stack.append(w+b)
    return len(stack) == 0

w3, w12 = 9, 1
for w5, w6 in [(2,9),(1,8)]:
    for w7, w8 in [(9,2),(8,1)]:
        for w4, w9 in [(9,7),(8,6),(7,5),(6,4),(5,3),(4,2),(3,1)]:
            for w10,w11 in [(9,6),(8,5),(7,4),(6,3),(5,2),(4,1)]:
                for w2,w13 in [(4,9),(3,8),(2,7),(1,6)]:
                    for w1 in range(9,0,-1):
                        w14 = w1
                        ws = [w1,w2,w3,w4,w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 ]
                        if simulate(ws):
                            print(''.join(map(str,ws)))

