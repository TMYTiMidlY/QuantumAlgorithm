import numpy as np
import qalgo as qa
from qalgo import qda
from matplotlib import pyplot as plt


def generate(zero=True) -> tuple[np.ndarray, np.ndarray]:
    if zero:
        A = np.array(
            [
                [1, 2, 3, 0, 4],
                [2, 1, 4, 0, 5],
                [3, 4, 1, 0, 6],
                [0, 0, 0, 0, 0],
                [4, 5, 6, 0, 1.0],
            ]
        )
        b = np.array([3, 4.5, 11.8, 0, 0.2])
    else:
        A = np.array(
            [
                [1, 2, 3, 4],
                [2, 1, 4, 5],
                [3, 4, 1, 6],
                [4, 5, 6, 1.0],
            ]
        )
        b = np.array([3, 4.5, 11.8, 0.2])

    return A, b


def test_entire_process():
    A, b = generate(zero=False)

    A_q, b_q, recover_x = qda.classical2quantum(A, b)

    x_q = qda.solve(A_q, b_q, kappa=qa.condest(A))
    print(f"{x_q = }")
    x_hat = recover_x(x_q)

    # minimize || b - norm A x_hat ||, get norm of x
    y = np.dot(A, x_hat)
    norm = np.dot(b, y) / np.dot(y, y)

    x = norm * x_hat

    x_reference = np.linalg.solve(A_q, b_q)
    x_reference_hat = x_reference / np.linalg.norm(x_reference)

    print(f"{x = }")
    print(f"{x_reference = }")
    print(f"{x_hat = }")
    print(f"{x_reference_hat = }")
    assert np.allclose(x_hat, x_reference_hat, rtol=1e-1), (
        "The solution does not match the reference solution."
    )
