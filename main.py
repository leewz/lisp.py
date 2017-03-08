#!/usr/bin/env python3

import sys
from read import READ, refresh
from lisp import LISPSCOPE
from debuggery import log
import numerics


def readfile(scope, fname):
    with open(fname) as f: #load the startup file.
        refresh(f)
        try:
            while True:
                scope.EVAL(READ())
        except StopIteration:
            return

def REPL(scope):
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


if __name__ == '__main__':
    # (LOOP (PRINT (EVAL (READ))))
    scope = LISPSCOPE()
    readfile(scope, 'startup.lpy')
    if len(sys.argv) == 1:
        REPL(scope)
    else:
        readfile(scope, sys.argv[1])


