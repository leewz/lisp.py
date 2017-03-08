class peekiter:
    NONE = object()
    def __init__(self, iterable):
        self._iter = iter(iterable)
        self._next = self.NONE
    def peek(self, default=NONE):
        if self._next is self.NONE:
            self._next = next(self._iter, default)
        if self._next is self.NONE:
            raise StopIteration
        return self._next
    def __iter__(self):
        return self
    def __next__(self):
        val, self._next = self.peek(), self.NONE
        return val
    def putback(self, val):
        if self._next is not self.NONE:
            assert 0
        self._next = val
