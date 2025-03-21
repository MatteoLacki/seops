import functools


def compose_from_left(*funcs):
    """Compose functions from left to right.

    So that compose(f,g,h)(x) == h(g(f(x)))
    """
    return lambda x: functools.reduce(lambda v, f: f(v), funcs, x)


def compose_from_right(*funcs):
    """Compose functions from right to left.

    So that compose(f,g,h)(x) == f(g(h(x)))
    """
    return lambda x: functools.reduce(lambda v, f: f(v), reversed(funcs), x)
