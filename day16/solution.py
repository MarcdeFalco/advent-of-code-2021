from math import prod

class BitStream:
    def __init__(self, data):
        self.data = data

        def get_bit(s):
            for i in range(len(s)):
                c = eval('0x'+s[i])
                cb = bin(c)[2:]
                cb = '0'*(4-len(cb)) + cb
                for b in cb:
                    yield b

        self.gen = get_bit(self.data)

    def get_bits(self, n):
        s = ''
        for i in range(n):
            s += next(self.gen)
        return s

    def get_litteral(self):
        lit = 0
        size = 0
        while True:
            header = self(1)
            value = self(4)
            size += 5
            lit = 16 * lit + value
            if header == 0:
                break
        return (lit, size)

    def __call__(self, n):
        return eval('0b'+self.get_bits(n))

class Packet:
    def __init__(self, version, pid, size, subpackets=None):
        self.version = version
        self.pid = pid
        self.size = size
        if subpackets is None:
            self.subpackets = []
        else:
            self.subpackets = subpackets

    def cumulative_version(self):
        v = self.version
        for packet in self.subpackets:
            v += packet.cumulative_version()
        return v

class Litteral(Packet):
    def __init__(self, version, pid, size, lit):
        super().__init__(version, pid, size)
        self.lit = lit

    def value(self):
        return self.lit

class Operator(Packet):
    def __init__(self, version, pid, size, subpackets):
        super().__init__(version, pid, size, subpackets=subpackets)

    def value(self):
        sub_values = ( sub.value() for sub in self.subpackets )

        if self.pid == 0:
            return self.sum(*sub_values)
        if self.pid == 1:
            return self.prod(*sub_values)
        if self.pid == 2:
            return self.min(*sub_values)
        if self.pid == 3:
            return self.max(*sub_values)
        if self.pid == 5:
            return self.gt(*sub_values)
        if self.pid == 6:
            return self.lt(*sub_values)
        if self.pid == 7:
            return self.eq(*sub_values)

        raise ValueError

    def sum(self, *l): return sum(l)
    def prod(self, *l): return prod(l)
    def min(self, *l): return min(l)
    def max(self, *l): return max(l)
    def gt(self, a, b):
        if a > b:
            return 1
        else:
            return 0
    def lt(self, a, b):
        if a < b:
            return 1
        else:
            return 0
    def eq(self, a, b):
        if a == b:
            return 1
        else:
            return 0

def read_packet(b):
    version = b(3)
    pid = b(3)
    size = 6
    if pid == 4:
        lit, lit_size = b.get_litteral()
        size += lit_size
        return Litteral(version, pid, size, lit)
    else:
        length_id = b(1)
        size += 1
        sub = []
        if length_id == 0:
            length = b(15)
            size += 15 + length
            while length > 0:
                p = read_packet(b)
                sub.append(p)
                length -= p.size
        else:
            count = b(11)
            size += 11
            for _ in range(count):
                p = read_packet(b)
                sub.append(p)
                size += p.size
        return Operator(version, pid, size, sub)

    def version(self):
        return self.version + sum(sp.version() for sp in p.sub)

bitstream = BitStream(open('input.txt').read().strip())
p = read_packet(bitstream)

print('Part 1', p.cumulative_version())
print('Part 2', p.value())
