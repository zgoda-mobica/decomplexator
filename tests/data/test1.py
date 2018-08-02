def fun1(x, y):
    return x + y


def fun2(x, y):
    if x > 2:
        raise ValueError('Too much!')
    return y ^ x
