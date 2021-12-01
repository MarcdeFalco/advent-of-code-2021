depths = [ int(l) for l in open('input.txt') ]

increased = 0
for i in range(1, len(depths)):
    if depths[i] > depths[i-1]:
        increased += 1

print('Part 1', increased)

increased = 0
window = depths[0] + depths[1] + depths[2]
for i in range(3, len(depths)):
    new_window = window - depths[i-3] + depths[i]
    if new_window > window:
        increased += 1
    window = new_window

print('Part 2', increased)
