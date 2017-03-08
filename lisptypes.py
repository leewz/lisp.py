class OBJECT:
    def __init__(self, vtype, value):
        self.type = vtype
        self.value = value
    def __repr__(self):
        return "%s(%s)" % (self.type.__name__, self.value)

def unwrap(val):
    return getattr(val, 'value', val)

def istype(val, typ):
    return getattr(val, 'type', None) is typ

def SYMBOL(s): #symbol type
    #? Do I want `(SYMBOL x)` or `(SYMBOL 'x)`?
        # The second, because `(SYMBOL x)` will use the string in x.
    s = s.upper()
    try:
        sym = SYMBOL.cache[s]
    except KeyError:
        SYMBOL.cache[s] = sym = OBJECT(SYMBOL, s)
        sym.__name__ = s
    return sym

SYMBOL.cache = {}


T = SYMBOL('T')
NIL = SYMBOL('NIL')


def CONS(car, cdr):
    return OBJECT(CONS, (car, cdr))




