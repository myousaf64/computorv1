#!/usr/bin/env python3
"""Computor v1 - solve a polynomial equation of degree <= 2.

No math library is used for the roots: sqrt is implemented by hand (Newton's
method), as the subject only allows +, -, *, / that you implemented yourself.
Coefficients are kept as exact fractions so cancellation lands on a true zero.
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


def solve(coeffs, degree, out):
    a = float(coeffs.get(2, 0))
    b = float(coeffs.get(1, 0))
    c = float(coeffs.get(0, 0))
    if degree == 0:
        # ponytail: degree-0 prints no "Polynomial degree" line, per subject examples
        out('Any real number is a solution.' if c == 0 else 'No solution.')
        return
    out(f'Polynomial degree: {degree}')
    if degree > 2:
        out("The polynomial degree is strictly greater than 2, I can't solve.")
    elif degree == 1:
        out('The solution is:')
        out(g(-c / b))
    else:
        disc = b * b - 4 * a * c
        if disc > 0:
            root = my_sqrt(disc)
            out('Discriminant is strictly positive, the two solutions are:')
            out(g((-b - root) / (2 * a)))
            out(g((-b + root) / (2 * a)))
        elif disc == 0:
            out('Discriminant is zero, the solution is:')
            out(g(-b / (2 * a)))
        else:
            re_ = -b / (2 * a)
            im = my_sqrt(-disc) / (2 * a)
            out('Discriminant is strictly negative, the two complex solutions are:')
            out(f'{g(re_)} + {g(abs(im))}i')
            out(f'{g(re_)} - {g(abs(im))}i')


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
