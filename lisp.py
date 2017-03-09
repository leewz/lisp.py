# Lisp interpreter in Python, 2017 attempt.
# This isn't a specific Lisp dialect.


from dictutil import register, Scope
from read import READ
from lisptypes import *


def macro(f):
    # f.type = MACRO
    # f.value = f.__name__
    f.ismacro = True
    return f

def register_macro(d, key=None):
    reg0 = register(d, key)
    def registrar(value):
        reg0(value)
        return macro(value)
    return registrar



###########

# Universal constants.
names = {}
register(names)(READ)
register(names)(SYMBOL)
register(names)(CONS)
register(names)(T)
register(names)(NIL)


class LISPSCOPE(Scope):
    def __init__(scope, parent=None):
        if parent is None:
            parent = names
            scope.root = scope
        else:
            scope.root = parent.root
        super().__init__(parent)

    def EVAL(scope, val):
        """ """
        # If it's a literal, just return the literal.
        if isVALUE(val):
            return val
        # If it's a single symbol, resolve it.
        if istype(val, SYMBOL):
            return scope[val.value]
        # If it's a list, evaluate the head and apply it to the tail.
        if istype(val, CONS):
            head = CAR(val)
            tail = CDR(val)
            f = scope.EVAL(head)
            return scope.callthing(f, tail)
        #??
        if callable(val):
            return val
        assert False

    def callthing(scope, f, args):
        if not isMACRO(f):
            # Evaluate the args.
            args = scope.map(scope.EVAL, args)
        rv = scope.docall(f, args)
        if isMACRO(f) and not callable(f):
            rv = scope.EVAL(rv)
        if rv is None or rv is False:
            return NIL
        elif rv is True:
            return T
        else:
            return rv

    def docall(scope, f, args):
        # Call without evaluating args.
        if callable(f):
            return f(*tolist(args))
        return f.scope.WITH(f.params, args, f.body)
            #! Does this leak outer params into the function call?

    def map(scope, f, lst):
        # Needed for argument evaluation.
        if NILP(lst):
            return NIL
        assert istype(lst, CONS)
        return CONS(f(CAR(lst)), scope.map(f, CDR(lst)))

    def SETNAME(scope, sym, value):
        #? Is this scoped?
        #scope[sym.value.upper()] = value
        scope.root[sym.value.upper()] = value
        return value

    @macro
    def FUNCTION(scope, params, body):
        obj = OBJECT(FUNCTION, [params, body])
        obj.params = params
        obj.body = body
        obj.scope = scope #for closures.
        return obj

    @macro
    def MACRO(scope, params, body):
        # A macro takes in unevaluated args and returns a transformed thing to evaluate.
        obj = OBJECT(MACRO, [params, body])
        obj.params = params
        obj.body = body
        obj.scope = scope #??
        return obj
        #TODO: "Clean" macros.
        #TODO: Embed names.

    @macro
    def WITH(scope, params, args, body):
        #? Is this "LABELS"?
        newscope = LISPSCOPE(scope)
        newscope.assign(params, args)
        return newscope.EVAL(body)

    def assign(scope, params, args):
        if NILP(params):
            assert NILP(args)
        elif istype(params, SYMBOL):
            scope[params.value.upper()] = args
        else:
            scope.assign(CAR(params), CAR(args))
            scope.assign(CDR(params), CDR(args))

    @macro
    def IF(scope, condition, then, otherwise=None):
        if not NILP(scope.EVAL(condition)):
            return scope.EVAL(then)
        elif otherwise is not None:
            return scope.EVAL(otherwise)
        else:
            return NIL

    def PRINT(scope, val):
        print(scope.tostr(val))

    def tostr(scope, val):
        if isinstance(val, str):
            return '"%s"' % val
        elif isVALUE(val):
            return str(val)
        elif callable(val): #It's a function.
            return val.__name__
        elif not isinstance(val, OBJECT):
            return repr(val)
        elif istype(val, SYMBOL):
            return val.value
        elif istype(val, CONS):
            return scope.tostr_CONS(val)
        elif istype(val, FUNCTION) or istype(val, MACRO):
            # I want to look up its name in the scope.
            try:
                return scope.getname(val)
            except ValueError: #lol
                return repr(val)
        else:
            raise NotImplementedError(val.type)

    def getname(scope, val):
        try:
            return val.__name__
        except AttributeError: pass
        scp = scope
        while isinstance(scp, LISPSCOPE):
            try:
                return _getkey(scp.d, val)
            except KeyError: pass
            scp = scp.parent
        return _getkey(scp, val) #last try

    def tostr_CONS(scope, val):
        return '(%s)' % ' '.join(map(scope.tostr, tolist(val)))

def _getkey(d, val):
    for k, v in d.items():
        if v is val:
            return k
    raise ValueError(val)



# Ugh, types.
FUNCTION = LISPSCOPE.FUNCTION
MACRO = LISPSCOPE.MACRO

#Aliases
setattr(LISPSCOPE, '=', LISPSCOPE.SETNAME)

def isVALUE(val):
    #return val not in
    return isinstance(val, (int, float, str))

def isMACRO(val):
    return istype(val, MACRO) or getattr(val, 'ismacro', False)

def tolist(val):
    """ Lisp list to Python list.
    """
    lst = []
    while istype(val, CONS):
        lst.append(CAR(val))
        val = CDR(val)
        if NILP(val):
            break
        if not istype(val, CONS):
            lst.append(SYMBOL('.'))
            lst.append(val)
            break
    return lst


@register(names)
def LOOP(*args): #??
    ...


@register(names)
def CAR(cell):
    return cell.value[0]


@register(names)
def CDR(cell):
    return cell.value[1]


@register_macro(names)
def QUOTE(val):
    return val


@register(names)
def EQ(x, y):
    return unwrap(x) == unwrap(y)
    #! Doesn't make () == NIL!

@register(names)
def ATOM(val):
    return not istype(val, CONS)


@register(names, 'NIL?')
def NILP(val):
    return val is NIL


