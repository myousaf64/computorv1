"""Self-check against the subject's worked examples. Run: python3 test_computor.py"""
from computor import run


def output(equation):
    lines = []
    run(equation, out=lines.append)
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

    print(f"OK: {len(CASES)} cases pass")
