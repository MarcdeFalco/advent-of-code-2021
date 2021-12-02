pos, depth = 0, 0

for l in open('input.txt'):
    dire, amount = l.strip().split()
    amount = int(amount)
    if dire == 'forward':
        pos += amount
    if dire == 'up':
        depth -= amount
    if dire == 'down':
        depth += amount

print('Part 1', pos * depth)

pos, depth, aim = 0, 0, 0

for l in open('input.txt'):
    dire, amount = l.strip().split()
    amount = int(amount)
    if dire == 'forward':
        pos += amount
        depth += aim * amount
    if dire == 'up':
        aim -= amount
    if dire == 'down':
        aim += amount

print('Part 1', pos * depth)
print('Part 2', pos * depth)
