# Decisions

One entry for each decision that constrains later work. Newest first.
A locked decision stays locked. Do not propose an alternative unless the
decision now breaks.

## Template

```
## YYYY-MM-DD - <the decision>

**Context:** what forced a choice.
**Decision:** what we chose.
**Because:** the reason.
**Instead of:** the option we rejected, and why.
```

---

## 2026-09-05 - No dev branch

**Context:** `AGENTS.md` named `dev` as the integration branch, but all seven
pull requests were opened against `main` and merged into `main`. `dev` never
had a copy on the remote.
**Decision:** `main` is the only long-lived branch. One branch for each task,
branched from `main`, merged into `main` by a pull request.
**Because:** One person works on this repository and the whole check is one
command that runs in under a second. An integration branch adds a merge step
and protects nothing.
**Instead of:** Keeping `dev` and rewriting the history of seven merged pull
requests to match a rule that nobody followed.

## 2026-09-04 - Every bonus prints behind a flag

**Context:** The subject assesses the bonus only if the mandatory part is
perfect, and the mandatory output is compared against the screenshots.
**Decision:** Free form entry is always on. The other five bonus features print
only with `--steps`, `--fractions`, `--verbose` or `--plot`.
**Because:** A default run then stays byte-identical to the six worked
examples, and `test_computor.py` asserts that.
**Instead of:** Printing the irreducible fraction next to every decimal, which
changes the mandatory output and fails the comparison.

## 2026-09-04 - One grammar reads both entry forms

**Context:** Free form entry is a bonus, and a second parser would double the
number of places a term can be dropped.
**Decision:** One scanner. The coefficient, the `*` and the `^n` are each
optional, so `5 * X^0` and a bare `5` take the same path.
**Because:** The canonical form is a special case of the free form, so one
grammar is smaller and cannot disagree with itself.
**Instead of:** A regular expression per form. The old single regex silently
skipped every term it did not match, which hid three defects.

## 2026-09-04 - Exact rational arithmetic, float only at print time

**Context:** `0.1 * X^0 + 0.3 * X^1 + 0.225 * X^2 = 0` has an exact
discriminant of zero. Computed in `float` it reads `-1.39e-17`, so the program
printed two complex solutions instead of one double root.
**Decision:** Coefficients, the discriminant and the roots stay `Fraction`.
`g()` converts to `float` once, to print.
**Because:** The sign of the discriminant decides the branch. A sign that comes
from rounding noise is a correctness bug, not a display bug.
**Instead of:** A tolerance such as `abs(disc) < 1e-9`. A tolerance invents a
new wrong answer for coefficients near that scale, and cannot be justified at
a defense.

## 2026-09-04 - Square roots written by hand

**Context:** The subject forbids a math library function that you did not
implement.
**Decision:** `int_sqrt` is Newton's method on whole numbers. `exact_sqrt` runs
it on the numerator and the denominator of a fraction. `my_sqrt` runs the same
iteration on floats.
**Because:** `int_sqrt` keeps a perfect square exact, so `sqrt(16)` is `4` and
not `4.000000000000001`, and no import is needed.
**Instead of:** `math.sqrt` or `math.isqrt`. Both are library functions and both
invite the same question at a defense.
