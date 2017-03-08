#!/usr/bin/env python3

from read import READ, refresh
from lisp import LISPSCOPE
from debuggery import log
import numerics

if __name__ == '__main__':
    # (LOOP (PRINT (EVAL (READ))))
    scope = LISPSCOPE()
    with open('startup.lpy') as f: #load the startup file.
        refresh(f)
        try:
            while True:
                scope.EVAL(READ())
        except StopIteration: pass
    refresh()
    while True:
        print('>>>', end=' ', flush=True)
        val = READ()
        log('READ:', scope.tostr(val))
        try:
            result = scope.EVAL(val)
        except KeyError as e:
            print("UNDEFINED SYMBOL:", e.args[0])
        else:
            print('=>', end=' ')
            scope.PRINT(result)

