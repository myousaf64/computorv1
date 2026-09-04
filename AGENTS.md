# AGENTS.md

Read this file before you change the repository. Update it when the
architecture or the workflow changes.

`CLAUDE.md` is a symlink to this file. Claude, Codex, and Kimi read the same
contract.

## What this project is

`computorv1`, a 42 Abu Dhabi project. One program reads a polynomial equation,
reduces it, reports the degree, and solves it when the degree is 2 or lower.
Subject: `computorv1.en.subject.pdf`, version 6.3.

The mandatory part is complete. The bonus part is complete: free form entry
plus five features, each behind a flag.

## Stack

| Layer | Choice |
|---|---|
| Language | Python 3, standard library only |
| Build | none, `computor.py` runs directly |
| Test | `test_computor.py`, assert based, no framework |

## Setup

```sh
# No setup. Python 3.8 or later is the only requirement.
python3 --version
```

## Run locally

```sh
python3 computor.py "5 * X^0 + 4 * X^1 = 4 * X^0"
echo "5 * X^0 + 4 * X^1 = 4 * X^0" | python3 computor.py
python3 computor.py --help
```

The guide at `docs/computorv1-explained.html` opens in a browser from
`file://`. It needs no build step and no server.

## Verify

Run these before you open a pull request. Put the output in the pull request
body.

```sh
python3 test_computor.py     # 32 checks, all six subject examples byte for byte
python3 -m py_compile computor.py test_computor.py
```

## Git workflow

`main` is stable. `dev` is the integration branch. One branch for each task,
branched from `dev`, merged into `dev` by a pull request.

Full rules: `~/dotfiles/claude/WORKFLOW.md`. The rules are enforced by
`~/dotfiles/claude/hooks/guard-git.sh`, not by this paragraph.

An agent never merges a pull request.

## Agent roles

| Agent | Owns |
|---|---|
| Claude | Planning, review, architecture decisions |
| Codex | Implementation against an approved plan |
| Kimi | Frontend work and research |

One agent owns one branch. Two agents never share a branch.

## Constraints

- No math library function that the subject forbids. `int_sqrt` and `my_sqrt`
  are Newton iterations written in `computor.py`. The file imports `sys` and
  `fractions`, nothing else.
- Coefficients, the discriminant and the roots stay `Fraction` values. Only
  `g()` converts to `float`, at print time. A `float` discriminant reports the
  wrong sign for decimal coefficients.
- The default output must stay byte-identical to the six subject examples.
  Every bonus prints behind a flag.
- `docs/computorv1-explained.html` is one self-contained file. No build step,
  no framework, no CDN script. Google Fonts is the only external request.

## More

| Document | Holds |
|---|---|
| `docs/architecture.md` | Structure, modules, data flow |
| `docs/decisions.md` | Decisions taken and the reason for each |
| `docs/workflow.md` | Anything about the process that is specific to this repository |
| `docs/computorv1-explained.html` | Interactive guide: maths, code, defects, defense notes |
| `~/dotfiles/claude/WORKFLOW.md` | Branch, commit, pull request, and CI rules shared by every repository |

Continuous integration follows the shared policy: light checks on a pull
request, the expensive build and deploy only on a version tag. Do not restate it
here. Record a deviation in `docs/workflow.md` with its reason.

## Current state

- Mandatory part: done and verified against the six subject examples.
- Bonus part: free form entry, entry mistakes, `--fractions`, `--steps`,
  `--verbose`, `--plot`.
- Five defects found and fixed. Each one has a test. See `docs/decisions.md`.
