from typing import Tuple

import numpy as np

VARIANT = (
    (55.0, 0.0, 0.0),
    (-0.2, 0.002, 0.0),
    (0.7, 0.5, -0.2),
)
B = (13, 42, 21)

print("VARIANT =", VARIANT)

print("====")


def runtest(
    Ai: int = None,
    Aj: int = None,
    bi: int = None,
    e: float = 0.1,
) -> Tuple[float, float, np.ndarray]:
    b = list(B)
    variant = [[c for c in row] for row in VARIANT]
    if Ai is not None and Aj is not None:
        variant[Ai][Aj] += e

    if bi is not None:
        b[bi] += e

    A = np.array(variant, np.float32)
    b = np.array(b, np.float32)

    x = np.linalg.solve(A, b)

    print("A:")
    print(A)
    print("x = b / A:")
    print(x)

    print("====")
    y1 = np.linalg.cond(A)
    print("y1 = cond(A) =", y1)

    print("====")
    eigs = np.linalg.eigvals(A)
    print("eigs =", eigs)
    max_eig = max(eigs)
    print("max(eigs) =", max_eig)
    min_eig = min(eigs)
    print("min(eigs) =", min_eig)
    y2 = max_eig / min_eig
    print("y2 = max(eigs) / min(eigs) =", y2)

    return y1, y2, x


if __name__ == "__main__":
    y1, y2, x = runtest(e=0)
    results = [{
        "i": None,
        "j": None,
        "b": None,
        "e": 0.0,
        "y1": y1,
        "y2": y2,
        "x": x,
    }]
    for e in (0.1, -0.1):
        for i in range(len(VARIANT)):
            for j in range(len(VARIANT[i])):
                res = runtest(Ai=i, Aj=j, e=e)
                results.append({
                    "i": i,
                    "j": j,
                    "b": None,
                    "e": e,
                    "y1": res[0],
                    "y2": res[1],
                    "x": res[2],
                })
    for e in (0.1, -0.1):
        for b in range(len(B)):
            res = runtest(bi=b, e=e)
            results.append({
                "i": None,
                "j": None,
                "b": b,
                "e": e,
                "y1": res[0],
                "y2": res[1],
                "x": res[2],
            })

    print("=====")
    print("=====")
    print("=====")
    print("A: ")
    for i in range(len(VARIANT)):
        for j in range(len(VARIANT[i])):
            print(f"{VARIANT[i][j]:^12}", end="")
        print()
    print("b:", B)
    print("=====")
    print("results:")

    print(
        " i | j | b |    e   |        val        |"
        "                y1                |                y2                "
        "|                x"
    )
    for res in results:
        i = res["i"]
        j = res["j"]
        b = res["b"]
        e = f"{res['e']:+.1f}"
        val = "-"
        if i is not None and j is not None:
            val = f"{VARIANT[res['i']][res['j']]}({e:<4})"
        else:
            i = "-"
            j = "-"

        if b is not None:
            val = f"{B[res['b']]}({e:<4})"
        else:
            b = "-"

        print(
            "", i, "|",
            j, "|",
            b, "|",
            f"{e:^6}", "|",
            f"{val:^17}", "|",
            f"{res['y1']:^32.6f}", "|",
            f"{res['y2']:^32.6f}", "|"
            f"{str(res['x']):^48}", "|"
            f"{str(x - res['x']):^48}",
        )
