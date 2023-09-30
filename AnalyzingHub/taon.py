data = [[0.1, 0.02, 0.01], [0.16, 0.12, 0.08], [0.2, 0.17, 0.14]]

sum = 0
for x in range(1, 4):
    for y in range(0, 3):
       sum += x*y*data[x - 1][y]
print(sum)