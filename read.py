import sys
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

def READ(end=''):
    """ Reads a string and returns a parsed Lisp value.
    """
    #. Eat leading spaces.
    skip_spaces()
    c = next(stream)
    log("C", c)
    if c in end:
        return None
    elif c in readtable:
        val = readtable[c](end)
    else: #Anything else.
        #stream.putback(c)
        val = read_SYMBOL(c, end)
    if val is None:
        return READ(end) #try again.
    return val


def skip_spaces():
    while stream.peek().isspace():
        next(stream)


def read_SYMBOL(s, end):
    """ Read until space or something.

    s is what's already been read.
    Numbers are symbols, too.
    """
    log('read_SYMBOL', s, end)
    for c in stream:
        #! Be careful about reading too far.
        if c.isspace():
            break
        if c in end:
            stream.putback(c)
            break
        s += c
    log("SYMBOL", s)
    try: return int(s)
    except ValueError: pass
    try: return float(s)
    except ValueError: pass
    return SYMBOL(s)


@register(readtable, "(")
def read_LIST(end):
    log("read_LIST")
    # a list is a cons cell chain
    end = set(end) | set(')')
    val = READ(end)
    if val is None:
        return NIL
    elif val is SYMBOL('.'):
        #return read_LIST(end)
        cdr = READ(end) #expects a ')' right after.
        assert READ(end) is None
        return cdr
        #? How should I specify "expects this after"?
    else:
        return CONS(val, read_LIST(end))


@register(readtable, "'")
def read_QUOTE(end):
    return CONS(SYMBOL('QUOTE'), CONS(READ(end), NIL))


@register(readtable, ";")
def read_COMMENT(end):
    for c in stream:
        if c == '\n':
            break
    return


@register(readtable, '"')
def read_STRING(end):
    s = ''
    for c in stream:
        if c == '"':
            break
        s += c
    return s


@register(readtable, '#')
def read_POUND(end):
    ...


def istream(file):
    for line in file:
        yield from line


def refresh(file=None):
    global stream
    stream = peekiter(istream(file or sys.stdin))

refresh()


