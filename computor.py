#!/usr/bin/env python3
"""Computor v1 - solve a polynomial equation of degree 2 or lower.

The arithmetic is exact. Coefficients, the discriminant and the roots stay
Fraction values, so a discriminant that is truly zero reads as zero and not as
a small negative float. No math library computes a root: int_sqrt and my_sqrt
are hand-written Newton iterations, as the subject allows only the four
operations that you implement yourself.
"""
import sys
import re
from fractions import Fraction

TERM = re.compile(r'([+-]?)\s*([\d.]+)\s*\*\s*[Xx]\s*\^\s*(\d+)')


def parse(equation):
    """Return {degree: Fraction coeff} for lhs - rhs, given canonical terms."""
    lhs, rhs = equation.split('=')
    coeffs = {}
    for side, sign in ((lhs, 1), (rhs, -1)):
        for s, num, exp in TERM.findall(side):
            c = Fraction(num) * (-1 if s == '-' else 1) * sign
            coeffs[int(exp)] = coeffs.get(int(exp), 0) + c
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
