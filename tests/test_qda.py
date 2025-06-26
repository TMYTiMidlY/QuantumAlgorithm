import numpy as np
import qalgo as qa
from qalgo import qda
import pysparq as sq

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
    sq.System.clear()

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
    assert np.allclose(x_hat, x_reference_hat, rtol=0.1), (
        "The solution does not match the reference solution."
    )


def test_classical2quantum():
    sq.System.clear()

    A, b = generate(zero=True)
    A_q, b_q, recover_x = qda.classical2quantum(A, b)
    _A_q, _b_q, _recover_x = qda._classical2quantum(A, b)
    assert np.allclose(A_q, _A_q), "Quantum matrix A_q should match _A_q."
    assert np.allclose(b_q, _b_q), "Quantum vector b_q should match _b_q."

    assert A_q.shape == (8, 8), "Quantum matrix A_q should be 4x4."
    assert b_q.shape == (8,), "Quantum vector b_q should have length 4."
    assert callable(recover_x), "recover_x should be a callable function."

    x_q = qda.solve(A_q, b_q, kappa=qa.condest(A))
    x_hat = recover_x(x_q)
    _x_hat = _recover_x(x_q)

    assert np.allclose(x_hat, _x_hat), "Recovered vector x_hat should match _x_hat."

    assert x_hat.shape == (5,), "Recovered vector x_hat should have length 5."


def test_solve():
    sq.System.clear()

    A, b = generate(zero=False)

    A_q, b_q, recover_x = qda.classical2quantum(A, b)

    x_q = qda.solve(A_q, b_q, kappa=qa.condest(A))
    _x_q = qda._solve(A_q, b_q, kappa=qa.condest(A))

    assert np.allclose(x_q, _x_q[4:8]), "Quantum solution x_q should match _x_q."

    assert x_q.shape == (4,), "Recovered vector x_hat should have length 4."
