import sys
from dataclasses import dataclass
from typing import (
    ClassVar,
    Iterable,
    Optional,
    Tuple,
)

from prettytable import PrettyTable
from random import uniform


TYPE_K1 = "min"
TYPE_K2 = "max"
TYPE_K3 = "min"

ALTERNATIVE_AMOUNT = 200

DECIMAL_PLACES = 3

# VARIANT #1
RANGE_K1 = (5.4, 7.9)
RANGE_K2 = (0.9, 0.99)
RANGE_K3 = (23.1, 45.8)

CRITERIA_PRIORITY = (1, 3, 2)

DEFAULT_CONCESSION = 0.2

# VARIANT #15
# RANGE_K1 = (7.5, 12.8)
# RANGE_K2 = (0.91, 0.97)
# RANGE_K3 = (17.9, 27.4)
#
# CRITERIA_PRIORITY = (3, 1, 2)
#
# DEFAULT_CONCESSION = 0.3


def get_best_and_worst(kn: int):
    options = [min, max]
    func_type = globals()[f"TYPE_K{kn}"]
    range_vals = globals()[f"RANGE_K{kn}"]

    best, worst = options.pop(func_type == "max"), options.pop()

    return best(range_vals), worst(range_vals)


@dataclass
class Alternative:
    i: int
    k1: float
    k2: float
    k3: float

    e1: Optional[float] = None
    e2: Optional[float] = None
    e3: Optional[float] = None

    pareto_better: Optional[Tuple[int, "Alternative"]] = None

    headers: ClassVar[Iterable[str]] = (
        "i",
        "k1",
        "k2",
        "k3",
        "e1",
        "e2",
        "e3",
        "worse_then",
    )

    @classmethod
    def get_properties(cls) -> Iterable[str]:
        return cls.headers

    @property
    def worse_then(self):
        if self.pareto_better is None:
            return None

        return self.pareto_better[0]

    def __gt__(self, other):
        if not isinstance(other, Alternative):
            raise TypeError(f"Can not compare Alternative and {type(other)}")

        if not all((
            self.e1 is not None,
            self.e2 is not None,
            self.e3 is not None,
            other.e1 is not None,
            other.e2 is not None,
            other.e3 is not None,
        )):
            raise NotImplementedError(
                "Can only compare E-values, call .count_e() method before",
            )

        return all((
            self.e1 > other.e1,
            self.e2 > other.e2,
            self.e3 > other.e3,
        ))

    def to_dict(self):
        obj = {}
        for prop in self.get_properties():
            obj[prop] = getattr(self, prop)

        return obj

    def count_e(self):
        for i in range(1, 4):
            best, worst = get_best_and_worst(i)
            ki = getattr(self, f"k{i}")
            ei = (ki - worst) / (best - worst)

            setattr(self, f"e{i}", round(ei, DECIMAL_PLACES))


class AlternativesAmountError(RuntimeError):
    pass


def generate_alternatives() -> Iterable[Alternative]:
    for index in range(ALTERNATIVE_AMOUNT):
        k = []
        for i in range(1, 4):
            rng_range = globals()[f"RANGE_K{i}"]
            rnd = uniform(rng_range[0], rng_range[1])
            k.append(round(rnd, DECIMAL_PLACES))

        yield Alternative(index, *k)


def count_e(
    alternatives: Iterable[Alternative],
) -> Iterable[Alternative]:
    for x in alternatives:
        x.count_e()

        yield x


def count_pareto_efficient(
    alternatives: Iterable[Alternative],
) -> Iterable[Alternative]:
    alternatives = list(alternatives)
    for i in range(0, len(alternatives)):
        current = alternatives[i]
        for j in range(0, len(alternatives)):
            other = alternatives[j]
            if i == j:
                continue

            if current > other:
                other.pareto_better = (i, current)

        yield current


def filter_pareto_efficient(
    alternatives: Iterable[Alternative],
) -> Iterable[Alternative]:
    return filter(
        lambda x: x.pareto_better is None,
        alternatives,
    )


def filter_criteria_priority(
    k: int,
    alternatives: Iterable[Alternative],
) -> Iterable[Alternative]:
    concession = DEFAULT_CONCESSION
    alternatives = list(alternatives)
    best = max(alternatives, key=lambda x: getattr(x, f"e{k}"))
    best_ei = getattr(best, f"e{k}")
    for j in range(0, len(alternatives)):
        other = alternatives[j]
        ei = getattr(other, f"e{k}")
        if (best_ei - ei) <= concession:
            yield other


def filter_criteria_priority_all(
    alternatives: Iterable[Alternative],
) -> Iterable[Alternative]:
    for k in CRITERIA_PRIORITY:
        alternatives = filter_criteria_priority(
            k=k,
            alternatives=alternatives,
        )
        alternatives = list(alternatives)

        _print_iteration(
            header=f"Criteria priority filtered for criteria #{k}",
            alternatives=alternatives,
        )

        amount = len(alternatives)
        if amount <= 1 and k != CRITERIA_PRIORITY[-1]:
            raise AlternativesAmountError(
                f"Too few alternatives left: {amount}",
            )

    return alternatives


def main(*args):
    alternatives = generate_alternatives()
    alternatives = count_e(alternatives)
    alternatives = list(alternatives)
    _print_iteration(
        header="Alternatives generated",
        alternatives=alternatives,
    )

    alternatives = count_pareto_efficient(alternatives)
    alternatives = list(alternatives)
    _print_iteration(
        header="Pareto efficient calculated",
        alternatives=alternatives,
    )

    alternatives_pareto = list(alternatives)

    alternatives_pareto = filter_pareto_efficient(alternatives_pareto)
    alternatives_pareto = list(alternatives_pareto)
    _print_iteration(
        header="Pareto efficient filtered",
        alternatives=alternatives_pareto,
    )

    alternatives_pareto = filter_criteria_priority_all(alternatives_pareto)
    alternatives_pareto = list(alternatives_pareto)
    _print_iteration(
        header="Criteria priority filtered (pareto filtered)",
        alternatives=alternatives_pareto,
    )

    print()
    print()
    print("#" * 70)
    print(f"{'WITHOUT Pareto filter'.upper():^70}")
    print("#" * 70)
    print()
    print()

    alternatives = filter_criteria_priority_all(alternatives)
    alternatives = list(alternatives)
    _print_iteration(
        header="Criteria priority filtered (WITHOUT Pareto filter)",
        alternatives=alternatives,
    )

    return 0


def _print_iteration(
    header: str,
    alternatives: Iterable[Alternative],
):
    _print_section(f"{header}")

    table = _generate_table(alternatives)
    _print_table(table)


def _print_section(line: str):
    print("#" * 70)
    print(f"{line.upper():^70}")
    print("#" * 70)


def _print_table(table: PrettyTable):
    print(table)


def _generate_table(
    alternatives: Iterable[Alternative],
) -> PrettyTable:
    return _format_table(
        headers=Alternative.get_properties(),
        rows=map(lambda a: a.to_dict().values(), alternatives),
    )


def _format_table(
    headers: Iterable[str],
    rows: Iterable[Iterable[str]],
) -> PrettyTable:
    table = PrettyTable()
    table.field_names = headers
    for row in rows:
        table.add_row(list(row))

    return table


if __name__ == "__main__":
    sys.exit(main(*sys.argv))
