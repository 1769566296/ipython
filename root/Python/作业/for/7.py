

m = 0
for i in range(1, 4):
    for j in range(1, 4):
        if i > j:
            m += i + j
    print(m)
