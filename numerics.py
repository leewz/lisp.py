from lisp import names
from dictutil import register

@register(names, '+')#(sum)
def PLUS(x, y):
    return x + y


@register(names, '-')
def MINUS(x, y):
    return x - y

@register(names, '*')
def TIMES(x, y):
    return x * y

@register(names, '/')
def DIVIDE(x, y):
    return x / y






