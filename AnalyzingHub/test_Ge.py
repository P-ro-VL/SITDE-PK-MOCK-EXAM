P = 0.0
p = 0.05

times = 1
while P < 1:
    P = ((1 - 0.05) ** (times-1)) * 0.05
    print(times, P)
    times += 1
    if times >= 100:
        break
