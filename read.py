from iterutil import peekiter
from lisptypes import SYMBOL, CONS, NIL
from dictutil import register
from debuggery import log

__all__ = [
    'READ',
    'read_table',
]

readtable = {
}


def READ(src=None):
    """ Reads a string and returns a parsed Lisp value.
    """
    if src is None:
        src = stream
    else:
        src = peekiter(istream(src))
    return _read(src)


def _read(itr, end=''):
    #. Eat leading spaces.
    skip_spaces(itr)
    c = next(itr)
    log("C", c)
    if c in end:
        return None
    elif c in readtable:
        val = readtable[c](itr, end)
    else: #Anything else.
        val = read_SYMBOL(itr, c, end)
    if val is None:
        return _read(itr, end) #try again.
    return val


def skip_spaces(itr):
    while itr.peek().isspace():
        next(itr)


def read_SYMBOL(itr, s, end):
    """ Read until space or something.

    s is what's already been read.
    Numbers are symbols, too.
    """
    log('read_SYMBOL', s, end)
    for c in itr:
        if c.isspace():
            break
        if c in end:
            itr.putback(c)
            break
        s += c
    log("SYMBOL", s)
    try: return int(s)
    except ValueError: pass
    try: return float(s)
    except ValueError: pass
    return SYMBOL(s)


@register(readtable, "(")
def read_LIST(itr, end):
    log("read_LIST")
    # a list is a cons cell chain
    end = set(end) | set(')')
    val = _read(itr, end)
    if val is None:
        return NIL
    elif val is SYMBOL('.'): # CONS expression.
        cdr = _read(itr, end)
        assert cdr is not None and _read(itr, end) is None, "Expected exactly one item after a dot."
        return cdr
    else:
        return CONS(val, read_LIST(itr, end))


@register(readtable, "'")
def read_QUOTE(itr, end):
    return CONS(SYMBOL('QUOTE'), CONS(_read(itr, end), NIL))


@register(readtable, ";")
def read_COMMENT(itr, end):
    for c in itr:
        if c == '\n':
            break
    return


@register(readtable, '"')
def read_STRING(itr, end):
    s = ''
    for c in itr:
        if c == '"':
            break
        s += c
    return s


@register(readtable, '#')
def read_POUND(itr, end):
    raise NotImplementedError


def istream(file):
    for line in file:
        yield from line


def refresh(file):
    global stream
    stream = peekiter(istream(file))



