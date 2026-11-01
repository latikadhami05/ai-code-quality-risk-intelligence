def check(x):
    for i in range(x):
        if i % 2:
            for j in range(i):
                if j % 3:
                    print(j)
    return x
