def messy(a, b, c):
    result = 0
    for i in range(a):
        if i % 2:
            for j in range(b):
                if j % 3:
                    for k in range(c):
                        if k % 5:
                            while result < 10:
                                if i and j or k:
                                    result += 1
    return result
