"""Self-check for computor.py. Run: python3 test_computor.py

The first block asserts the subject's worked examples byte for byte. Any
difference there is a mandatory regression. The later blocks lock the five
defects that the first version had, and the bonus features.
"""
import subprocess
import sys

from computor import DEFAULTS, ParseError, run


def output(equation, **flags):
    lines = []
    opts = dict(DEFAULTS)
    opts.update(flags)
    run(equation, out=lines.append, opts=opts)
    return '\n'.join(lines)


# --------------------------------------------------------------------------
# mandatory: the six worked examples of the subject
# --------------------------------------------------------------------------

SUBJECT = {
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
    "1 * X^0 + 2 * X^1 + 5 * X^2 = 0": (
        "Reduced form: 1 * X^0 + 2 * X^1 + 5 * X^2 = 0\n"
        "Polynomial degree: 2\n"
        "Discriminant is strictly negative, the two complex solutions are:\n"
        "-0.2 + 0.4i\n-0.2 - 0.4i"),
}

# --------------------------------------------------------------------------
# the five defects that the first version had
# --------------------------------------------------------------------------

DEFECTS = {
    # A: the discriminant is exactly zero. A float discriminant read -1.4e-17
    #    and printed two complex solutions.
    "0.1 * X^0 + 0.3 * X^1 + 0.225 * X^2 = 0": (
        "Reduced form: 0.1 * X^0 + 0.3 * X^1 + 0.225 * X^2 = 0\n"
        "Polynomial degree: 2\n"
        "Discriminant is zero, the solution is:\n-0.666667"),
    # B: a root of zero printed as -0.
    "3 * X^1 = 0 * X^0": (
        "Reduced form: 0 * X^0 + 3 * X^1 = 0\n"
        "Polynomial degree: 1\nThe solution is:\n0"),
    "1 * X^2 = 0 * X^0": (
        "Reduced form: 0 * X^0 + 0 * X^1 + 1 * X^2 = 0\n"
        "Polynomial degree: 2\n"
        "Discriminant is zero, the solution is:\n0"),
    # C: scientific notation. The old regex read 1e10 as 10.
    "1e10 * X^0 + 1 * X^1 = 0": (
        "Reduced form: 1e+10 * X^0 + 1 * X^1 = 0\n"
        "Polynomial degree: 1\nThe solution is:\n-1e+10"),
}

# D and E: the parser raises instead of dropping a term or of crashing.
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

# --------------------------------------------------------------------------
# bonus
# --------------------------------------------------------------------------

FREE_FORM = {
    # The subject's bonus example.
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
}

# The last printed line of each run, with --fractions on.
FRACTIONS = {
    "5 * X^0 + 4 * X^1 = 4 * X^0": "-1/4 (-0.25)",
    "-4 * X^0 + 1 * X^2 = 0": "2",
    "1 * X^0 + 2 * X^1 + 5 * X^2 = 0": "-1/5 (-0.2) - 2/5 (0.4)i",
}


def check(got, expected, label):
    assert got == expected, (
        "\n%s\n--- expected ---\n%s\n--- got ---\n%s" % (label, expected, got))


def main():
    count = 0
    for equation, expected in list(SUBJECT.items()) + list(DEFECTS.items()) \
            + list(FREE_FORM.items()):
        check(output(equation), expected, equation)
        count += 1

    for equation, message in ERRORS.items():
        try:
            output(equation)
        except ParseError as error:
            check(str(error), message, equation)
        else:
            raise AssertionError('no ParseError for: %s' % equation)
        count += 1

    for equation, expected in FRACTIONS.items():
        line = output(equation, fractions=True).split('\n')[-1]
        check(line, expected, equation + ' --fractions')
        count += 1

    # The sqrt helpers agree with each other and need no math library.
    from computor import exact_sqrt, int_sqrt, my_sqrt
    from fractions import Fraction
    assert int_sqrt(0) == 0 and int_sqrt(1) == 1 and int_sqrt(2) == 1
    assert int_sqrt(10 ** 12) == 10 ** 6
    assert exact_sqrt(Fraction(9, 4)) == Fraction(3, 2)
    assert exact_sqrt(Fraction(2)) is None
    assert exact_sqrt(Fraction(-1)) is None
    assert abs(my_sqrt(2) - 1.4142135623730951) < 1e-15
    assert my_sqrt(0) == 0.0
    count += 1

    # The flags print extra lines and change no solution.
    plain = output("1 * X^0 + 2 * X^1 + 5 * X^2 = 0")
    for flag in ('steps', 'verbose', 'plot'):
        rich = output("1 * X^0 + 2 * X^1 + 5 * X^2 = 0", **{flag: True})
        assert len(rich) > len(plain), '--%s printed nothing extra' % flag
        assert plain.split('\n')[-1] in rich, '--%s changed the solution' % flag
        count += 1

    # The command line exits 1 and prints no traceback on a bad equation.
    done = subprocess.run([sys.executable, 'computor.py', 'hello'],
                          capture_output=True, text=True)
    assert done.returncode == 1, done
    assert done.stderr.startswith('error: '), done.stderr
    assert 'Traceback' not in done.stderr, done.stderr
    count += 1

    # STDIN carries the equation when no argument is present.
    done = subprocess.run([sys.executable, 'computor.py'],
                          input="5 * X^0 + 4 * X^1 = 4 * X^0\n",
                          capture_output=True, text=True)
    assert done.returncode == 0, done
    check(done.stdout.strip(), SUBJECT["5 * X^0 + 4 * X^1 = 4 * X^0"], 'stdin')
    count += 1

    print("OK: %d checks pass" % count)


if __name__ == '__main__':
    main()
