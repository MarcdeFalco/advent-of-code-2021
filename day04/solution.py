lines = [ l.strip() for l in open('input.txt').readlines() ]
numbers = list(map(int, lines[0].split(',')))

boards = []
i = 2
while i < len(lines):
    l = []
    while i < len(lines) and lines[i] != '':
        l.append( list(map(int, lines[i].split())) )
        i += 1
    i += 1
    boards.append(l)

def won(b):
    return any( all(b[i][j] is None for j in range(5)) \
            or all(b[j][i] is None for j in range(5)) for i in range(5) )

def score(b, trigger):
    return sum( sum(k for k in l if k is not None) for l in b ) * trigger

nboards = len(boards)
won_boards = [ None ] * nboards
won_order = []
for n in numbers:
    for k, b in enumerate(boards):
        if won_boards[k] is not None: continue
        for l in b:
            if n in l:
                l[l.index(n)] = None # strike n
                if won(b):
                    won_boards[k] = n
                    won_order.append(k)


kfirst = won_order[0]
bfirst = boards[kfirst]
print('Part 1', score(bfirst, won_boards[kfirst]))
klast = won_order[-1]
blast = boards[klast]
print('Part 2', score(blast, won_boards[klast]))
