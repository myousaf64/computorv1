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
    print(f"OK: {len(CASES)} cases pass")
