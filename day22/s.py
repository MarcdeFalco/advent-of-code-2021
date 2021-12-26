from itertools import permutations, product, combinations
from collections import defaultdict, Counter
import sys
sys.path.append("..")
from speedaoc import AOC

def povray_export(i, cuboids):
    f = open('cuboid_%04d.pov' % i, 'w')
    w = 200000
    b = 0.8
    f.write(f'''camera {{ location <-{w},0,-{w}>
            right image_width/image_height*x
    look_at <0,0,0> }}

#default {{finish{{ambient 0}} }}

    light_source {{ <0,0,-200000> color<0.8,1,1> }}
    light_source {{ <-200000,0,0> color<1,0.8,1> }}
    light_source {{ <-200000,0,-200000> color<1,1,1> }}


    ''')

    for cuboid in cuboids:
        cuboid.povray(f)

show = False
if show:
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.gca(projection='3d')

submit = False
if 'submit' in sys.argv:
    submit = True
part = 1
if '2' in sys.argv:
    part = 2

#print(submit, part)

aoc = AOC(22)
si = aoc.input
s = aoc.example

if submit:
    s = si

s = si
import re
r = re.compile(r'(on|off) x=(.*)\.\.(.*),y=(.*)\.\.(.*),z=(.*)\.\.(.*)')

steps = []
for l in  s.split('\n')[:-1]:
    m = r.match(l)
    t = tuple(m.groups())
    steps.append((t[0],) + tuple(map(int, t[1:])))

class Cuboid:
    def __init__(self, x1,x2,y1,y2,z1,z2):
        self.x = (x1,x2)
        self.y = (y1,y2)
        self.z = (z1,z2)

    def intersect(self, other):
        def inter(a,b,c,d):
            return not(b < c or d < a)

        x1, x2 = self.x
        y1, y2 = self.y
        z1, z2 = self.z
        ox1, ox2, oy1, oy2, oz1, oz2 = other.x + other.y + other.z
        return inter(x1,x2,ox1,ox2) and inter(y1,y2,oy1,oy2) and inter(z1,z2,oz1,oz2)

    def contains(self, other):
        def ct(a,b,c,d):
            return a <= c <= d <= b
        x1, x2 = self.x
        y1, y2 = self.y
        z1, z2 = self.z
        ox1, ox2, oy1, oy2, oz1, oz2 = other.x + other.y + other.z
        return ct(x1,x2,ox1,ox2) and ct(y1,y2,oy1,oy2) and ct(z1,z2,oz1,oz2)

    def remove(self, other):
        if not self.intersect(other):
            return [ self ]

        x1, x2 = self.x
        y1, y2 = self.y
        z1, z2 = self.z
        ox1, ox2, oy1, oy2, oz1, oz2 = other.x + other.y + other.z

        def split(x1, x2, r1, r2):
            if r1 <= x1 <= x2 <= r2:
                return [(x1,x2)]
            if x1 < r1 <= r2 < x2:
                return [ (x1,r1-1), (r1,r2), (r2+1,x2) ]
            if x1 <= r2 < x2:
                return [(x1,r2), (r2+1,x2)]
            if x1 < r1 <= x2:
                return [(x1,r1-1), (r1,x2)]
            return [(x1,x2)]

        xs = split(x1, x2, ox1, ox2)
        ys = split(y1, y2, oy1, oy2)
        zs = split(z1, z2, oz1, oz2)

        res = []
        for (x1,x2), (y1,y2), (z1,z2) in product(xs, ys, zs):
            sub_cuboid = Cuboid(x1,x2,y1,y2,z1,z2)
            #if other.contains(Cuboid(x1,x2,y1,y2,z1,z2)):
            #    continue

            if sub_cuboid.intersect(other):
                continue

            res.append( sub_cuboid )

        return res

    def on(self):
        x1, x2 = self.x
        y1, y2 = self.y
        z1, z2 = self.z
        return (1+x2-x1)*(1+y2-y1)*(1+z2-z1)

    def __repr__(self):
        return '(%d..%d,%d..%d,%d..%d)' % (self.x+self.y+self.z)

    def plot(self, color='b'):
        x1, x2 = self.x
        y1, y2 = self.y
        z1, z2 = self.z

        x1 -= 0.5
        y1 -= 0.5
        z1 -= 0.5
        x2 += 0.5
        y2 += 0.5
        z2 += 0.5

        ax.plot3D([x1,x1],[y1,y1],[z1,z2], color=color)
        ax.plot3D([x2,x2],[y1,y1],[z1,z2], color=color)
        ax.plot3D([x1,x1],[y2,y2],[z1,z2], color=color)
        ax.plot3D([x2,x2],[y2,y2],[z1,z2], color=color)

        ax.plot3D([x1,x1],[y1,y2],[z1,z1], color=color)
        ax.plot3D([x2,x2],[y1,y2],[z1,z1], color=color)
        ax.plot3D([x1,x1],[y1,y2],[z2,z2], color=color)
        ax.plot3D([x2,x2],[y1,y2],[z2,z2], color=color)

        ax.plot3D([x1,x2],[y1,y1],[z1,z1], color=color)
        ax.plot3D([x1,x2],[y2,y2],[z1,z1], color=color)
        ax.plot3D([x1,x2],[y1,y1],[z2,z2], color=color)
        ax.plot3D([x1,x2],[y2,y2],[z2,z2], color=color)

    def povray(self, f):
        x1, x2 = self.x
        y1, y2 = self.y
        z1, z2 = self.z
        s = '''box {
            <%f,%f,%f>,
            <%f,%f,%f>
            pigment { color<1,1,1> }
            }''' % (x1-0.5,y1-0.5,z1-0.5,x2+0.5,y2+0.5,z2+0.5)
        f.write(s + '\n')
            
cuboids = []
i = 0
for step in steps:
    status, x1,x2,y1,y2,z1,z2 = step
    current = Cuboid(x1,x2,y1,y2,z1,z2)
    old = cuboids

    cuboids = sum( (cuboid.remove(current) for cuboid in cuboids), [] )
    if status == 'on':
        cuboids.append( current )
    povray_export(i, cuboids)
    i += 1

if show:
    import matplotlib.colors as mcolors
    def colors():
        l = list(mcolors.CSS4_COLORS.keys())
        i = 0
        while True:
            yield(l[i])
            i += 1
            if i >= len(l):
                i = 0

    col = colors()
    for cuboid in cuboids:
        cuboid.plot(next(col))
    plt.show()

ans = sum(cuboid.on() for cuboid in cuboids)


