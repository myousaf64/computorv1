# computorv1 - progress

**Status: mandatory DONE and verified. Bonus DONE.**

## Mandatory

`computor.py` solves polynomial equations of degree 2 or lower: reduced form,
degree, discriminant sign, real and complex solutions. STDIN fallback when no
argument is present. Own `int_sqrt` and `my_sqrt`, no math library. Exact
`Fraction` coefficients, discriminant and roots.

## Bonus

- Free form entry, one grammar for both forms: `5 + 4 * X + X^2 = X^2`
- Entry mistakes: `error: <reason>` on stderr, exit 1, no traceback
- `--fractions` irreducible fraction solutions
- `--steps` intermediate calculation
- `--verbose` coefficient table of both sides
- `--plot` ASCII curve with the roots marked

## Defects found and fixed

| # | Input | Was | Fix |
|---|---|---|---|
| A | `0.1 * X^0 + 0.3 * X^1 + 0.225 * X^2 = 0` | D read as `-1.4e-17`, printed complex roots | D is a `Fraction`, exact sign |
| B | `3 * X^1 = 0 * X^0` | `-0` | `g()` adds `0.0` before `%g` |
| C | `1e10 * X^0 + 1 * X^1 = 0` | read as `10`, silently wrong | the scanner reads an exponent suffix |
| D | `5 * Y^0 = 0 * X^0` | term dropped, wrong answer | the scanner rejects leftover text |
| E | `hello` | Python traceback | `ParseError`, caught in `main()` |

Each defect has a test in `test_computor.py`.

## Verify

```sh
python3 test_computor.py     # OK: 32 checks pass
```

**Run:** `python3 computor.py "5 * X^0 + 4 * X^1 = 4 * X^0"` &middot; `echo "<eq>" | python3 computor.py`

## Guide

`docs/computorv1-explained.html`, a single self-contained page. Also published
as a private artifact: https://claude.ai/code/artifact/20666ce5-01b9-4164-bb94-54b18ceaa9b0
