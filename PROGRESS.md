# computorv1 - progress

**Status: mandatory DONE & verified.**

- `computor.py` - solves polynomial equations degree ≤2. Reduced form, degree,
  discriminant sign, real/complex solutions. STDIN fallback when no CLI arg.
  Own `my_sqrt` (Newton) - no math lib, per subject. Exact `Fraction` coeffs.
- `test_computor.py` - asserts all 6 subject worked examples. **Run:** `python3 test_computor.py`

**Run:** `python3 computor.py "5 * X^0 + 4 * X^1 = 4 * X^0"`  ·  `echo "<eq>" | python3 computor.py`

## Next (bonus, only if mandatory stays perfect)
- Free-form entry (`5 + 4 * X + X^2 = X^2`)
- Irreducible-fraction display of solutions (Fraction is already in place)
- Input-error handling (syntax/vocabulary)
- Intermediate calculation steps
