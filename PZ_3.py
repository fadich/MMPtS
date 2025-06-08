import sys

from PZ_2 import (
    Alternative,
    count_e,
    _print_iteration,
)


TYPE_K1 = "min"
TYPE_K2 = "max"
TYPE_K3 = "min"

RANGE_K1 = (5.0, 12.5)
RANGE_K2 = (0.8, 0.99)
RANGE_K3 = (21.2, 47.5)

ALPHA = 1

ALTERNATIVES = (
    Alternative(
        i=1,
        k1=7.6,
        k2=0.84,
        k3=23.1,
    ),
    Alternative(
        i=2,
        k1=10.4,
        k2=0.91,
        k3=26.3,
    ),
    Alternative(
        i=3,
        k1=10.3,
        k2=0.9,
        k3=43.6,
    ),
    Alternative(
        i=16,
        k1=5.7,
        k2=0.97,
        k3=27.5,
    ),
    Alternative(
        i=17,
        k1=6.2,
        k2=0.9,
        k3=41.5,
    ),
)


def main(*args):
    alternatives = count_e(ALTERNATIVES)
    alternatives = list(alternatives)
    for alternative in alternatives:
        alternative.e1 = round(alternative.e1 ** ALPHA, 2)
        alternative.e2 = round(alternative.e2 ** ALPHA, 2)
        alternative.e3 = round(alternative.e3 ** ALPHA, 2)

    _print_iteration(
        header="Alternatives generated",
        alternatives=alternatives,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv))
