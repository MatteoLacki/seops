import functools


def compose_from_left(*funcs):
    return lambda x: functools.reduce(lambda v, f: f(v), funcs, x)


def compose_from_right(*funcs):
    return lambda x: functools.reduce(lambda v, f: f(v), reversed(funcs), x)
