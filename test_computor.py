"""Self-check against the subject's worked examples. Run: python3 test_computor.py"""
from computor import DEFAULTS, run


def output(equation, **flags):
    lines = []
    opts = dict(DEFAULTS)
    opts.update(flags)
    run(equation, out=lines.append, opts=opts)
    return '\n'.join(lines)


CASES = {
    "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0": (
        "Reduced form: 4 * X^0 + 4 * X^1 - 9.3 * X^2 = 0\n"
        "Polynomial degree: 2\n"
        "Discriminant is strictly positive, the two solutions are:\n"
        "0.905239\n-0.475131"),
    "5 * X^0 + 4 * X^1 = 4 * X^0": (
        "Reduced form: 1 * X^0 + 4 * X^1 = 0\n"
        "Polynomial degree: 1\nThe solution is:\n-0.25"),
    "8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0": (
        "Reduced form: 5 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 0\n"
        "Polynomial degree: 3\n"
        "The polynomial degree is strictly greater than 2, I can't solve."),
    "6 * X^0 = 6 * X^0": (
        "Reduced form: 0 * X^0 = 0\nAny real number is a solution."),
    "10 * X^0 = 15 * X^0": (
        "Reduced form: -5 * X^0 = 0\nNo solution."),
    # Scientific notation. The old regex read 1e10 as 10.
    "1e10 * X^0 + 1 * X^1 = 0": (
        "Reduced form: 1e+10 * X^0 + 1 * X^1 = 0\n"
        "Polynomial degree: 1\nThe solution is:\n-1e+10"),
    # Free form entry. The subject's bonus example, then two shorter ones.
    "5 + 4 * X + X^2 = X^2": (
        "Reduced form: 5 * X^0 + 4 * X^1 = 0\n"
        "Polynomial degree: 1\nThe solution is:\n-1.25"),
    "5 + 4x = 4": (
        "Reduced form: 1 * X^0 + 4 * X^1 = 0\n"
        "Polynomial degree: 1\nThe solution is:\n-0.25"),
    "x^2 = 4": (
        "Reduced form: -4 * X^0 + 0 * X^1 + 1 * X^2 = 0\n"
        "Polynomial degree: 2\n"
        "Discriminant is strictly positive, the two solutions are:\n-2\n2"),
    # An exactly zero discriminant. A float discriminant read -1.4e-17 here
    # and printed two complex solutions.
    "0.1 * X^0 + 0.3 * X^1 + 0.225 * X^2 = 0": (
        "Reduced form: 0.1 * X^0 + 0.3 * X^1 + 0.225 * X^2 = 0\n"
        "Polynomial degree: 2\n"
        "Discriminant is zero, the solution is:\n-0.666667"),
    # An exact square root keeps the roots whole.
    "-4 * X^0 + 1 * X^2 = 0 * X^0": (
        "Reduced form: -4 * X^0 + 0 * X^1 + 1 * X^2 = 0\n"
        "Polynomial degree: 2\n"
        "Discriminant is strictly positive, the two solutions are:\n-2\n2"),
    # A root of zero must print 0, not -0.
    "3 * X^1 = 0 * X^0": (
        "Reduced form: 0 * X^0 + 3 * X^1 = 0\n"
        "Polynomial degree: 1\nThe solution is:\n0"),
    "1 * X^2 = 0 * X^0": (
        "Reduced form: 0 * X^0 + 0 * X^1 + 1 * X^2 = 0\n"
        "Polynomial degree: 2\n"
        "Discriminant is zero, the solution is:\n0"),
    "1 * X^0 + 2 * X^1 + 5 * X^2 = 0": (
        "Reduced form: 1 * X^0 + 2 * X^1 + 5 * X^2 = 0\n"
        "Polynomial degree: 2\n"
        "Discriminant is strictly negative, the two complex solutions are:\n"
        "-0.2 + 0.4i\n-0.2 - 0.4i"),
}

# Every one of these was a silent wrong answer or a traceback before.
ERRORS = {
    "5 * Y^0 = 0 * X^0": 'a "*" must be followed by X',
    "5 * X^-1 = 0": 'an exponent must be a whole number, 0 or more',
    "hello": 'an equation must have exactly one "="',
    "5 * X^0": 'an equation must have exactly one "="',
    "5 * X^0 = 1 = 2": 'an equation must have exactly one "="',
    "= 5": 'one side of the equation is empty',
    "5 + = 2": 'a term is missing at the end of a side',
    "5 & 3 = 0": 'unexpected symbol "&" - put a "+" or a "-" between two terms',
    ". = 0": 'a lone "." is not a number',
    "5 . 3 = 0": 'unexpected symbol "." - put a "+" or a "-" between two terms',
}


# The last printed line of each run, with --fractions on.
FRACTIONS = {
    "5 * X^0 + 4 * X^1 = 4 * X^0": "-1/4 (-0.25)",
    "-4 * X^0 + 1 * X^2 = 0": "2",
    "1 * X^0 + 2 * X^1 + 5 * X^2 = 0": "-1/5 (-0.2) - 2/5 (0.4)i",
}


if __name__ == '__main__':
    for eq, expected in CASES.items():
        got = output(eq)
        assert got == expected, f"\nEQ: {eq}\n--- expected ---\n{expected}\n--- got ---\n{got}"

    # The square roots are hand written. int_sqrt stays exact on whole numbers.
    from computor import exact_sqrt, int_sqrt, my_sqrt
    from fractions import Fraction
    assert int_sqrt(0) == 0 and int_sqrt(1) == 1 and int_sqrt(2) == 1
    assert int_sqrt(10 ** 12) == 10 ** 6
    assert exact_sqrt(Fraction(9, 4)) == Fraction(3, 2)
    assert exact_sqrt(Fraction(2)) is None
    assert exact_sqrt(Fraction(-1)) is None
    assert abs(my_sqrt(2) - 1.4142135623730951) < 1e-15
    assert my_sqrt(0) == 0.0

    # --fractions adds the irreducible form next to the decimal.
    for eq, expected in FRACTIONS.items():
        got = output(eq, fractions=True).split('\n')[-1]
        assert got == expected, f"\nEQ: {eq} --fractions\nGOT: {got}\nWANT: {expected}"

    # A flag prints extra lines and changes no solution.
    plain = output("1 * X^0 + 2 * X^1 + 5 * X^2 = 0")
    for flag in ('steps', 'verbose'):
        rich = output("1 * X^0 + 2 * X^1 + 5 * X^2 = 0", **{flag: True})
        assert len(rich) > len(plain), f"--{flag} printed nothing extra"
        assert plain.split('\n')[-1] in rich, f"--{flag} changed the solution"

    # A bad entry raises, with the reason.
    from computor import ParseError
    for eq, message in ERRORS.items():
        try:
            output(eq)
        except ParseError as error:
            assert str(error) == message, f"\nEQ: {eq}\nGOT: {error}\nWANT: {message}"
        else:
            raise AssertionError(f"no ParseError for: {eq}")

    # The command line exits 1 and prints no traceback.
    import subprocess
    import sys
    done = subprocess.run([sys.executable, 'computor.py', 'hello'],
                          capture_output=True, text=True)
    assert done.returncode == 1, done
    assert done.stderr.startswith('error: '), done.stderr
    assert 'Traceback' not in done.stderr, done.stderr

    # STDIN carries the equation when no argument is present.
    done = subprocess.run([sys.executable, 'computor.py'],
                          input="5 * X^0 + 4 * X^1 = 4 * X^0\n",
                          capture_output=True, text=True)
    assert done.returncode == 0, done
    assert done.stdout.strip() == CASES["5 * X^0 + 4 * X^1 = 4 * X^0"], done.stdout

    print(f"OK: {len(CASES)} cases and {len(ERRORS)} errors pass")
