# computorv1

Solves polynomial equations of degree 2 or lower. Prints the reduced form, the
degree, the sign of the discriminant and the real or complex solutions. A 42 Abu Dhabi project.

## Run

```
python3 computor.py "5 * X^0 + 4 * X^1 = 4 * X^0"
echo "5 * X^0 + 4 * X^1 = 4 * X^0" | python3 computor.py
```

## Test

```
python3 test_computor.py
```

Asserts all six worked examples from the assignment.

## Notes

- Square root is a hand-written Newton iteration; no math library, as the subject
  requires.
- Coefficients are exact `Fraction` values.
- `PROGRESS.md` is the development log and lists the remaining bonus work.
