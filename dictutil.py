
def register(d, key=None):
    def registrar(value):
        nonlocal key
        if key is None:
            key = value.__name__
        if isinstance(key, str):
            d[key] = value
        else:
            for k in key:
                d[k] = value
        return value
    return registrar


class Scope:
    """ Nested scope functionality.
    """
    def __init__(scope, parent=None):
        scope.d = dict()
        scope.parent = parent

    def __getitem__(scope, name):
        name = name.upper()
        try:
            return scope.d[name]
        except KeyError:
            #! The following repeats for nested scopes.
            val = getattr(scope, name, None)
            if val:
                return val
            try:
                return scope.parent[name]
            except KeyError:
                pass
            raise

    def __setitem__(scope, name, value):
        name = name.upper()
        scope.d[name] = value


