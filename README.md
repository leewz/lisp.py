Run `main.py` with no arguments to start the REPL.

    python main.py
Run with one argument to run a file.

    python main.py mylispcode.lsp

I'm not a real Lisper, so this isn't a real Lisp dialect. I used some of Arc Lisp's names.

Syntax:
- Case-insensitive.
- Literal strings (using `"`) and numbers (not fractions) are implemented.
    - Characters and backslash escapes are not implemented.
- A `'` quotes (i.e. leaves unevaluated) the next item, whether a literal or a list. E.g. `'A` has the value of the symbol `A`.
- A `.` before the last item makes that item the tail. E.g. `(CDR '(A B))` => `(B)`, but `(CDR '(A . B))` => `B`.
- Comments start with `;` and extend to the end of the line.

Semantics:
- This implementation is a [Lisp-1](http://stackoverflow.com/questions/4578574/what-is-the-difference-between-lisp-1-and-lisp-2), meaning functions and variables share the same namespace.

These functions are defined within the Python code:
- (READ): Read and parse a single object from standard input.
- (READ string): Parse a string into an object.
- (EVAL expr): Evaluate an item.
    - Symbols evaluate to their value in scope.
    - Lists evaluate as function/macro calls.
    - Literals evaluate to themselves.
- (PRINT val): Print a single value.
- (= name val): Assignment. Evaluates `name` to a symbol and `val` to a value, and assigns it in the current scope.
- (ATOM val): True if val is not a CONS cell.
- (CONS head tail): Creates a pair `(head . tail)`.
- (CAR lst): Gets the first part of a CONS pair. Usually the head of a list.
- (CDR lst): Gets the second part. Usually the tail of a list.
- (FUNCTION PARAMS BODY): Make an anonymous function (AKA a lambda) 
- (MACRO PARAMS BODY): Make an anonymous macro. A macro, when called, gets its args unevaluated, and its return value will be evaluated instead.
- T, NIL: Constants for True and False. NIL is also considered the empty list.
- (QUOTE val): `val` itself, without evaluating.
- (SYMBOL string): Creates a symbol. Two symbols with the same name are the same symbol.
- (EQ x y): Test if two values are equal.
- (IF cond then else): If `cond`, then `then`, else `else`. Only the successful branch is evaluated.

Basic numerical operators are defined in `numerics.py`. Other functions are defined in `startup.lpy`. `main.py` loads both.

Will probably hit Python's recursion limit.

Example:

    (= 'pi 3.1415926)
    (= 'area-circle (function (r) (* pi (* r r))))

