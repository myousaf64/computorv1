#!/usr/bin/env python3
"""Computor v1 - solve a polynomial equation of degree 2 or lower.

The arithmetic is exact. Coefficients, the discriminant and the roots stay
Fraction values, so a discriminant that is truly zero reads as zero and not as
a small negative float. No math library computes a root: int_sqrt and my_sqrt
are hand-written Newton iterations, as the subject allows only the four
operations that you implement yourself.
"""
import sys
from fractions import Fraction

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
    """Return {exponent: Fraction} for the reduced equation."""
    sides = equation.split('=')
    if len(sides) != 2:
        raise ParseError('an equation must have exactly one "="')
    left = parse_side(sides[0])
    right = parse_side(sides[1])
    coeffs = dict(left)
    for exponent, coeff in right.items():
        coeffs[exponent] = coeffs.get(exponent, Fraction(0)) - coeff
    return coeffs


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


def reduced_form(coeffs):
    degree = max((d for d, c in coeffs.items() if c != 0), default=0)
    parts = [f'{g(coeffs.get(0, 0))} * X^0']
    for d in range(1, degree + 1):
        c = coeffs.get(d, 0)
        parts.append(f'{"+" if c >= 0 else "-"} {g(abs(c))} * X^{d}')
    return ' '.join(parts) + ' = 0', degree


# --------------------------------------------------------------------------
# solving
# --------------------------------------------------------------------------

def solve(coeffs, degree, out):
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
        out('The solution is:')
        out(g(-c / b))
        return
    disc = b * b - 4 * a * c
    if disc > 0:
        r = root_of(disc)
        if isinstance(r, Fraction):
            first, second = (-b - r) / (2 * a), (-b + r) / (2 * a)
        else:
            top, bottom = float(-b), float(2 * a)
            first, second = (top - r) / bottom, (top + r) / bottom
        out('Discriminant is strictly positive, the two solutions are:')
        out(g(first))
        out(g(second))
    elif disc == 0:
        out('Discriminant is zero, the solution is:')
        out(g(-b / (2 * a)))
    else:
        real = -b / (2 * a)
        r = root_of(-disc)
        imaginary = r / (2 * a) if isinstance(r, Fraction) else r / float(2 * a)
        out('Discriminant is strictly negative, the two complex solutions are:')
        out('%s + %si' % (g(real), g(abs(imaginary))))
        out('%s - %si' % (g(real), g(abs(imaginary))))


def run(equation, out=print):
    coeffs = parse(equation)
    form, degree = reduced_form(coeffs)
    out(f'Reduced form: {form}')
    solve(coeffs, degree, out)


def main():
    if len(sys.argv) > 1:
        equation = sys.argv[1]
    else:
        equation = sys.stdin.readline().strip()
    if not equation:
        print('usage: computor "<equation>"  (or pipe one on stdin)')
        return
    run(equation)


if __name__ == '__main__':
    main()
