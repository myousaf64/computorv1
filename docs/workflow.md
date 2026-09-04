# Workflow

Only what is specific to this repository. The shared rules live in
`~/dotfiles/claude/WORKFLOW.md`. Do not copy them here.

## Local overrides

None. There is no continuous integration for this repository, because the whole
check is one command that runs in under a second:

```sh
python3 test_computor.py
```

## Release

There is no release. The repository itself is the submission. The 42 defense
reads the working tree of the default branch.

## Traps

- **The mandatory output is compared byte for byte.** Any change to a printed
  line must keep the six subject examples identical. `test_computor.py` asserts
  them; run it after every edit to `computor.py`.
- **Never compute the discriminant in `float`.** See `docs/decisions.md`.
  A `float` discriminant reports the wrong sign for decimal coefficients.
- **Degree 0 prints no `Polynomial degree` line.** The subject's own examples do
  not print one. This looks like a missing line, and it is not.
- **`docs/computorv1-explained.html` is generated content, but is edited as
  source.** It is a single self-contained file with no build step. Do not add a
  bundler, a framework or a CDN script to it.
- **A zero leading coefficient lowers the degree.** `0 * X^2 + 3 * X^1 = 0` is
  degree 1. Solving it as a quadratic divides by zero.
