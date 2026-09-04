#!/usr/bin/env python3
"""Computor v1 - solve a polynomial equation of degree 2 or lower.

The arithmetic is exact. Coefficients, the discriminant and the roots stay
Fraction values, so a discriminant that is truly zero reads as zero and not as
a small negative float. No math library computes a root: int_sqrt and my_sqrt
are hand-written Newton iterations, as the subject allows only the four
operations that you implement yourself.

Mandatory output is byte-identical to the subject examples. Every bonus is
behind a flag, so the default run never changes.
"""
import sys
from fractions import Fraction

USAGE = """usage: computor [options] "<equation>"

Read the equation from the argument. Read it from STDIN when no argument
is present.

options:
  --steps      Print the intermediate calculation.
  --fractions  Print each solution as an irreducible fraction.
  --verbose    Print the coefficient table of the two sides.
  -h, --help   Print this text."""

DIGITS = '0123456789'


class ParseError(Exception):
    """The input is not a valid equation."""


# --------------------------------------------------------------------------
# parsing
#
# One grammar reads the canonical form and the free form:
#
#   side := term (('+' | '-') term)*
#   term := [number] ['*'] [X ['^' whole number]]
#
# The scanner consumes the side from left to right. Any symbol that the
# grammar does not accept raises a ParseError, so no term is dropped in
# silence.
# --------------------------------------------------------------------------

def _skip(s, i):
    while i < len(s) and s[i] in ' \t':
        i += 1
    return i


def _number(s, i):
    """Return (Fraction, next index). Return (None, i) when no number is at i."""
    start = i
    while i < len(s) and s[i] in DIGITS:
        i += 1
    if i < len(s) and s[i] == '.':
        i += 1
        while i < len(s) and s[i] in DIGITS:
            i += 1
    if i == start:
        return None, start
    if s[start:i] == '.':
        raise ParseError('a lone "." is not a number')
    end = i
    if end < len(s) and s[end] in 'eE':
        j = end + 1
        if j < len(s) and s[j] in '+-':
            j += 1
        k = j
        while j < len(s) and s[j] in DIGITS:
            j += 1
        if j > k:
            end = j
    return Fraction(s[start:end]), end


def _term(s, i):
    """Parse one term. Return (coefficient, exponent, next index)."""
    coeff, i = _number(s, i)
    i = _skip(s, i)
    star = i < len(s) and s[i] == '*'
    if star:
        i = _skip(s, i + 1)
    if i < len(s) and s[i] in 'Xx':
        i = _skip(s, i + 1)
        exponent = 1
        if i < len(s) and s[i] == '^':
            i = _skip(s, i + 1)
            value, i = _number(s, i)
            if value is None or value < 0 or value.denominator != 1:
                raise ParseError('an exponent must be a whole number, 0 or more')
            exponent = int(value)
        return (Fraction(1) if coeff is None else coeff), exponent, i
    if star:
        raise ParseError('a "*" must be followed by X')
    if coeff is None:
        if i >= len(s):
            raise ParseError('a term is missing at the end of a side')
        raise ParseError('unexpected symbol "%s"' % s[i])
    return coeff, 0, i


def parse_side(s):
    """Return {exponent: Fraction} for one side of the equation."""
    i = _skip(s, 0)
    if i >= len(s):
        raise ParseError('one side of the equation is empty')
    sign = 1
    if s[i] in '+-':
        sign = -1 if s[i] == '-' else 1
        i = _skip(s, i + 1)
    coeffs = {}
    while True:
        coeff, exponent, i = _term(s, i)
        coeffs[exponent] = coeffs.get(exponent, Fraction(0)) + sign * coeff
        i = _skip(s, i)
        if i >= len(s):
            return coeffs
        if s[i] not in '+-':
            raise ParseError('unexpected symbol "%s" - put a "+" or a "-" '
                             'between two terms' % s[i])
        sign = -1 if s[i] == '-' else 1
        i = _skip(s, i + 1)


def parse(equation):
    """Return (reduced coefficients, left coefficients, right coefficients)."""
    sides = equation.split('=')
    if len(sides) != 2:
        raise ParseError('an equation must have exactly one "="')
    left = parse_side(sides[0])
    right = parse_side(sides[1])
    coeffs = dict(left)
    for exponent, coeff in right.items():
        coeffs[exponent] = coeffs.get(exponent, Fraction(0)) - coeff
    return coeffs, left, right


# --------------------------------------------------------------------------
# arithmetic without a math library
# --------------------------------------------------------------------------

def int_sqrt(n):
    """Return the integer square root of n by Newton's method."""
    if n < 2:
        return n
    x, y = n, (n + 1) // 2
    while y < x:
        x, y = y, (y + n // y) // 2
    return x


def exact_sqrt(value):
    """Return the exact square root of a Fraction, or None when it is irrational."""
    if value < 0:
        return None
    top, bottom = int_sqrt(value.numerator), int_sqrt(value.denominator)
    if top * top == value.numerator and bottom * bottom == value.denominator:
        return Fraction(top, bottom)
    return None


def my_sqrt(value):
    """Return the square root of a number by Newton's method."""
    x = float(value)
    if x <= 0:
        return 0.0
    guess = x if x >= 1 else 1.0
    for _ in range(80):
        better = (guess + x / guess) / 2
        if better == guess:
            break
        guess = better
    return guess


def root_of(value):
    """Return the exact square root when it exists, else the float one."""
    exact = exact_sqrt(value)
    return exact if exact is not None else my_sqrt(value)


# --------------------------------------------------------------------------
# formatting
# --------------------------------------------------------------------------

def g(x):
    """Format a number like the subject examples. Never print a negative zero."""
    return '%g' % (float(x) + 0.0)


def show(value, opts):
    """Format a solution. Add the irreducible fraction when --fractions is on."""
    if opts['fractions'] and isinstance(value, Fraction):
        return str(value) if value.denominator == 1 else '%s (%s)' % (value, g(value))
    return g(value)


def reduced_form(coeffs):
    """Return (the reduced form text, the degree)."""
    degree = max((d for d, c in coeffs.items() if c != 0), default=0)
    parts = ['%s * X^0' % g(coeffs.get(0, Fraction(0)))]
    for d in range(1, degree + 1):
        c = coeffs.get(d, Fraction(0))
        parts.append('%s %s * X^%d' % ('+' if c >= 0 else '-', g(abs(c)), d))
    return ' '.join(parts) + ' = 0', degree


# --------------------------------------------------------------------------
# solving
# --------------------------------------------------------------------------

def coefficient_table(coeffs, left, right, out):
    """Print every collected term per side, so a reader can check the reduction."""
    out('Coefficients:')
    out('  X^n | left       | right      | left - right')
    for d in sorted(set(left) | set(right) | set(coeffs)):
        out('  %3d | %10s | %10s | %s' % (
            d, left.get(d, Fraction(0)), right.get(d, Fraction(0)),
            coeffs.get(d, Fraction(0))))


# --------------------------------------------------------------------------
# solving
# --------------------------------------------------------------------------


def solve(coeffs, degree, out, opts):
    a = coeffs.get(2, Fraction(0))
    b = coeffs.get(1, Fraction(0))
    c = coeffs.get(0, Fraction(0))
    if degree == 0:
        # The subject prints no degree line for a degree 0 equation.
        out('Any real number is a solution.' if c == 0 else 'No solution.')
        return
    out('Polynomial degree: %d' % degree)
    if degree > 2:
        out("The polynomial degree is strictly greater than 2, I can't solve.")
        return
    if degree == 1:
        if opts['steps']:
            out('[steps] b = %s, c = %s' % (b, c))
            out('[steps] b * X + c = 0, so X = -c / b = -(%s) / (%s)' % (c, b))
        root = -c / b
        roots = [root]
        out('The solution is:')
        out(show(root, opts))
        return
    disc = b * b - 4 * a * c
    if opts['steps']:
        out('[steps] a = %s, b = %s, c = %s' % (a, b, c))
        out('[steps] discriminant = b^2 - 4*a*c = (%s)^2 - 4*(%s)*(%s) = %s'
            % (b, a, c, disc))
        out('[steps] the discriminant is exact, so its sign is exact')
    if disc > 0:
        r = root_of(disc)
        if opts['steps']:
            out('[steps] sqrt(%s) = %s%s' % (disc, r,
                                             '' if isinstance(r, Fraction) else ' (Newton)'))
            out('[steps] X = (-b -+ sqrt(D)) / (2*a), 2*a = %s' % (2 * a))
        roots = [(-b - r) / (2 * a), (-b + r) / (2 * a)]
        out('Discriminant is strictly positive, the two solutions are:')
        out(show(roots[0], opts))
        out(show(roots[1], opts))
    elif disc == 0:
        if opts['steps']:
            out('[steps] X = -b / (2*a) = -(%s) / (%s)' % (b, 2 * a))
        roots = [-b / (2 * a)]
        out('Discriminant is zero, the solution is:')
        out(show(roots[0], opts))
    else:
        real = -b / (2 * a)
        r = root_of(-disc)
        imaginary = r / (2 * a)
        if opts['steps']:
            out('[steps] sqrt(-D) = sqrt(%s) = %s' % (-disc, r))
            out('[steps] X = -b / (2*a) -+ i * sqrt(-D) / (2*a)')
        roots = [complex(float(real), float(abs(imaginary))),
                 complex(float(real), -float(abs(imaginary)))]
        out('Discriminant is strictly negative, the two complex solutions are:')
        out('%s + %si' % (show(real, opts), show(abs(imaginary), opts)))
        out('%s - %si' % (show(real, opts), show(abs(imaginary), opts)))
    return


def run(equation, out=print, opts=None):
    opts = DEFAULTS if opts is None else opts
    coeffs, left, right = parse(equation)
    if opts['verbose']:
        coefficient_table(coeffs, left, right, out)
    form, degree = reduced_form(coeffs)
    out('Reduced form: %s' % form)
    solve(coeffs, degree, out, opts)


FLAGS = {'--steps': 'steps', '--fractions': 'fractions',
         '--verbose': 'verbose'}
DEFAULTS = {name: False for name in FLAGS.values()}


def main(argv):
    opts = dict(DEFAULTS)
    args = []
    for arg in argv:
        if arg in FLAGS:
            opts[FLAGS[arg]] = True
        elif arg in ('-h', '--help'):
            print(USAGE)
            return 0
        elif arg[:1] == '-' and len(arg) > 1 and arg[1] not in DIGITS + '.':
            print('error: unknown option "%s"' % arg, file=sys.stderr)
            print(USAGE, file=sys.stderr)
            return 1
        else:
            args.append(arg)
    if len(args) > 1:
        print('error: give exactly one equation', file=sys.stderr)
        return 1
    equation = args[0] if args else sys.stdin.readline().strip()
    if not equation:
        print(USAGE, file=sys.stderr)
        return 1
    try:
        run(equation, opts=opts)
    except ParseError as error:
        print('error: %s' % error, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
