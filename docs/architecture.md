# Architecture

Update this file when the structure changes.

## Layout

| Path | Holds |
|---|---|
| `computor.py` | The whole program. Parser, exact arithmetic, solver, formatting, CLI. |
| `test_computor.py` | Assert based checks. The six subject examples, the five fixed defects, the bonus output. |
| `docs/computorv1-explained.html` | Single file interactive guide. Opens from `file://`. |
| `computorv1.en.subject.pdf` | The assignment, version 6.3. |

## Data flow

Text goes in, printed lines come out. Nothing loops back.

1. `parse_side` scans one side, character by character, into terms.
2. `parse` splits on `=`, then subtracts the right coefficients from the left
   ones. The result is `{exponent: Fraction}` for `P(X) = 0`.
3. `reduced_form` prints the reduced equation and returns the degree.
4. `solve` branches on the degree: 0, 1, 2, or above 2.
5. `root_of` returns an exact `Fraction` square root when one exists, else a
   float from `my_sqrt`.
6. `g` converts to `float` and formats with `%g`. This is the only conversion.

A `ParseError` at stage 1 or 2 stops the run. `main` prints
`error: <reason>` on stderr and exits 1.

## External services

None. The program imports `sys` and `fractions`, nothing else.
