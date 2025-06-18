from typing import Callable

import numpy as np

import pysparq as sq
from . import wrapper
from . import utils

_classical2quantum = sq.qda_classical2quantum
_solve = wrapper.qda_solve


def classical2quantum(
    A_c: np.ndarray, b_c: np.ndarray
) -> tuple[np.ndarray, np.ndarray, Callable[[np.ndarray], np.ndarray]]:
    """
    Convert a classical linear system Ax = b to quantum-compatible form

    Returns:
        A_q: Quantum-compatible matrix (Hermitian, power-of-2 dimension)
        b_q: Corresponding right-hand side vector
        recover_x: Function to recover original solution from quantum solution
    """
    if A_c.shape[0] != A_c.shape[1]:
        raise ValueError("Input matrix A_c must be square.")
    if A_c.shape[0] != b_c.size:
        raise ValueError("Dimensions of A_c and b_c are incompatible.")

    original_dim = A_c.shape[0]
    hermitian_transform_done = False

    # Step 1: Hermitization (if necessary)
    # A simple check, though the problem implies it might not be
    # For robustness, we can always apply the embedding if not explicitly told it's Hermitian.
    # Or, if A_c IS Hermitian, we can skip. For now, let's assume we check.
    # A more robust check than `is_hermitian` for very small matrices or specific structures
    # might be needed, but `np.allclose` is generally good.
    if utils.is_hermitian(A_c):
        print("Input A is already Hermitian.")
        A_herm = A_c.copy()
        b_herm = b_c.copy()
    else:
        print("Input A is not Hermitian. Applying transformation.")
        hermitian_transform_done = True
        n = A_c.shape[0]
        A_herm = np.zeros((2 * n, 2 * n), dtype=A_c.dtype)
        A_herm[:n, n:] = A_c
        A_herm[n:, :n] = A_c.conj().T

        b_herm = np.zeros(2 * n, dtype=A_c.dtype)
        b_herm[:n] = b_c

    # Step 2: Padding to power of 2
    herm_dim = A_herm.shape[0]
    padded_dim = utils.next_power_of_2(herm_dim)

    if padded_dim == herm_dim:
        print("Dimension is already a power of 2.")
        A_q = A_herm
        b_q = b_herm
    else:
        print(f"Padding dimension from {herm_dim} to {padded_dim}")
        A_q = np.identity(padded_dim, dtype=A_herm.dtype)
        b_q = np.zeros(padded_dim, dtype=b_herm.dtype)

        A_q[:herm_dim, :herm_dim] = A_herm
        b_q[:herm_dim] = b_herm

    # Step 3: Create the recovery function
    def recover_x(x_q: np.ndarray) -> np.ndarray:
        if x_q.size != padded_dim:
            print(x_q.size,padded_dim)
            raise RuntimeError(
                "Solution vector x_q has incorrect dimension for recovery."
            )

        x_herm = x_q[:herm_dim].copy()

        if hermitian_transform_done:
            # Original x was in the second half of the [0, x]^T solution vector
            # for the system [0 A; A_dag 0] [y; z] = [b; 0]
            # where solution is y=0, z=x. So x_herm = [0; x]
            # and herm_dime == 2 * original_dim in this case.
            if x_herm.size != 2 * original_dim:
                raise RuntimeError(
                    "Mismatch in dimensions during hermitian recovery logic."
                )
            return x_herm[original_dim:]
        else:
            # No hermitian transform was done, x_herm is directly the solution
            # (potentially padded, but x_herm[:original_dim] already handled that)
            # and herm_dim == original_dim in this case.
            if x_herm.size != original_dim:
                raise RuntimeError(
                    "Mismatch in dimensions during non-hermitian recovery logic."
                )
            return x_herm
    
    return A_q, b_q, recover_x


# def solve(A:np.ndarray,b:np.ndarray) -> np.ndarray:
solve = _solve
