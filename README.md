# computorv1

Solves polynomial equations of degree 2 or lower. Prints the reduced form, the
degree, the sign of the discriminant and the real or complex solutions.
A 42 Abu Dhabi project.

## Run

```
python3 computor.py "5 * X^0 + 4 * X^1 = 4 * X^0"
echo "5 * X^0 + 4 * X^1 = 4 * X^0" | python3 computor.py
python3 computor.py --help
```

## Test

```
python3 test_computor.py
```

32 checks: the six worked examples of the subject byte for byte, the five fixed
defects, the parser error messages, and the bonus output.

## Bonus

Free form entry is always on: `python3 computor.py "5 + 4 * X + X^2 = X^2"`.
Five more features print behind a flag.

| Flag | Prints |
|---|---|
| `--steps` | The intermediate calculation. |
| `--fractions` | Each solution as an irreducible fraction. |
| `--verbose` | The coefficient table of the two sides. |
| `--plot` | The curve, drawn with ASCII characters, roots marked. |

Entry mistakes print `error: <reason>` on stderr and exit 1. No traceback.

## Guide

`docs/computorv1-explained.html` is an interactive single file guide: the maths,
the pipeline, a live solver, a discriminant explorer, the code walkthrough, the
edge cases, and the defense answers. Open it in a browser, no build step.

## Notes

- Square roots are hand-written Newton iterations. The file imports `sys` and
  `fractions`, nothing else.
- Coefficients, the discriminant and the roots stay exact `Fraction` values.
  Only printing converts to `float`.
- `PROGRESS.md` is the development log.
