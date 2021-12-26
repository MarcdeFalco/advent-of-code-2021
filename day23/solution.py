from collections import defaultdict
from queue import PriorityQueue
from functools import total_ordering

initial = open('input.txt').read().replace('\n','')
w, h = 13, len(initial)//13
solved_board = '##############...........####A#B#C#D###' \
        + '  #A#B#C#D#  ' * (h - 4) \
        + '  #########  '

class Move:
    def __init__(self, color, src, tgt):
        self.color = color
        self.src = src
        self.tgt = tgt

    def cost(self):
        cx = abs(self.tgt[0]-self.src[0])
        cy = abs(self.tgt[1]-self.src[1])
        cm = 10 ** 'ABCD'.index(self.color)
        return cm * (cx + cy)

@total_ordering
class Board:
    def __init__(self, flat_board, score=0):
        self.flat_board = flat_board
        self.score = score

    def __getitem__(self, c):
        x, y = c
        return self.flat_board[y * w + x]

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, other):
        return self.score == other.score

    def move(self, x, y):
        c = self[x, y]
        i = 'ABCD'.index(c)
        tgt_x = 3 + 2 * i

        if y == 1: # main row
            path_x = range(tgt_x,x) if tgt_x < x else range(x+1,tgt_x)
            if all(self[tx,y] == '.' for tx in path_x):
                if all(self[tgt_x,ty] in [c,'.'] for ty in range(2,h-1)):
                    lowest = max(ty for ty in range(2,h-1) if self[tgt_x,ty] == '.')
                    return [ Move(c, (x, y), (tgt_x, lowest)) ]
        elif all(self[x,ty] == '.' for ty in range(2,y)):
            if x != tgt_x or not all(self[x,ty] == c for ty in range(y+1,h-1)):
                valid_x = []
                x_l = x-1
                while self[x_l,1] == '.':
                    valid_x.append(x_l)
                    x_l -= 1
                x_r = x+1
                while self[x_r,1] == '.':
                    valid_x.append(x_r)
                    x_r += 1
                return [ Move(c, (x, y), (tx, 1)) 
                        for tx in valid_x if tx not in [3,5,7,9] ]

        return []

    def moves(self):
        return sum((self.move(i%w, i//w) for i, c in enumerate(self.flat_board)
                if c in 'ABCD'), [])

    def apply(self, move):
        csrc = move.src
        isrc = w * csrc[1] + csrc[0]
        ctgt = move.tgt
        itgt = w * ctgt[1] + ctgt[0]
        c = self.flat_board[isrc]
        if isrc < itgt:
            new_board = self.flat_board[:isrc] + '.' \
                    + self.flat_board[isrc+1:itgt] + c + self.flat_board[itgt+1:]
        else:
            new_board = self.flat_board[:itgt] + c \
                    + self.flat_board[itgt+1:isrc] + '.' + self.flat_board[isrc+1:]
        return Board(new_board, self.score+move.cost())

    def solved(self): return self.flat_board == solved_board

    def __hash__(self):
        return hash(self.flat_board)

b = Board(initial)
tovisit = PriorityQueue()
tovisit.put( b )
visited = defaultdict(bool)

best = 10**10
best_board = None
while not tovisit.empty():
    b = tovisit.get()
    if b.score > best or visited[b]: continue
    visited[b] = True
    if b.solved():
        if b.score < best:
            best = b.score
            best_board = b
    else:
        for move in b.moves():
            tovisit.put(b.apply(move))
    
print(best)
