from typing import Callable

import numpy as np
import pysparq as sq
from numpy.typing import NDArray

from . import utils, wrapper

_classical2quantum = sq.qda_classical2quantum
# _solve = wrapper.qda_solve


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
            print(x_q.size, padded_dim)
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


def compute_step_rate(step_rate: float, kappa: float) -> int:
    StepConstant = 2305
    steps = int(step_rate * StepConstant * kappa)
    if steps % 2 != 0:
        steps += 1  # 保证为偶数
    return steps


def scale_and_convert_vector(
    input_vec: NDArray[np.float64], exponent: int, data_size: int
) -> NDArray[np.uint64]:
    """
    Scale a floating-point vector, round to the nearest integer,
    and convert to unsigned integers using modular complement representation.

    Parameters:
    - input_vec: 1D numpy array of float64 values
    - exponent: scaling exponent (multiply by 2^exponent)
    - data_size: bit-width of the target representation (e.g., 8, 16, 32, 64)

    Returns:
    - A numpy array of uint64 values representing the scaled and converted input
    """
    scale = 2.0**exponent
    scaled_values = np.rint(input_vec * scale).astype(np.int64)

    # Apply make_complement to each value
    output = np.array(
        [utils.make_complement(value, data_size) for value in scaled_values],
        dtype=np.uint64,
    )
    return output


def make_vector_tree(dist: NDArray[np.uint64], data_size: int) -> NDArray[np.uint64]:
    """
    Constructs a vector tree based on the given distance vector and data size.

    Parameters:
    - dist: A numpy array of uint64 representing the distance vector.
    - data_size: An integer representing the size of the data in bits.

    Returns:
    - A numpy array of uint64 representing the constructed vector tree.
    """
    dist_sz = len(dist)
    temp_tree = dist.copy()
    tree = []

    while dist_sz > 1:
        temp = []
        for i in range(0, dist_sz, 2):
            if i + 1 < dist_sz:  # Avoid overflow
                if dist_sz == len(dist):
                    # Leaf nodes, calculated using get_complement
                    temp.append(
                        utils.get_complement(temp_tree[i], data_size) ** 2
                        + utils.get_complement(temp_tree[i + 1], data_size) ** 2
                    )
                else:
                    # Non-leaf nodes, sum directly
                    temp.append(temp_tree[i] + temp_tree[i + 1])

        # Combine all nodes
        temp.extend(temp_tree)
        temp_tree = np.array(temp, dtype=np.uint64)
        dist_sz = (dist_sz + 1) // 2  # Update dist_sz to match the layers

    temp_tree = np.append(temp_tree, np.uint64(0))  # Add a final zero to the tree
    tree.extend(temp_tree)
    return np.array(tree, dtype=np.uint64)


# solve = _solve
def solve(
    A: np.ndarray,
    b: np.ndarray,
    kappa: float = 0,
    p: float = 1.3,
    step_rate: float = 0.1,
) -> np.ndarray:
    if kappa == 0:
        kappa = utils.condest(A)
    steps = compute_step_rate(step_rate, kappa)

    data_size = 50
    rational_size = 51

    exponent = 15
    log_column_size = int(np.ceil(np.log2(A.shape[0])))

    conv_A = scale_and_convert_vector(A.flatten(order="F"), exponent, data_size)
    conv_b = scale_and_convert_vector(b, exponent, data_size)
    data_tree_A = make_vector_tree(conv_A, data_size)
    data_tree_b = make_vector_tree(conv_b, data_size)
    addr_size = log_column_size * 2 + 1

    qram_A = sq.QRAMCircuit_qutrit(addr_size, data_size, data_tree_A)
    qram_b = sq.QRAMCircuit_qutrit(log_column_size + 1, data_size, data_tree_b)

    print("QRAMCircuit ok")

    state = sq.SparseState()

    main_reg = sq.AddRegister(
        "main_reg", sq.StateStorageType.UnsignedInteger, log_column_size
    )(state)
    anc_UA = sq.AddRegister(
        "anc_UA", sq.StateStorageType.UnsignedInteger, log_column_size
    )(state)
    anc_4 = sq.AddRegister("anc_4", sq.StateStorageType.Boolean, 1)(state)
    anc_3 = sq.AddRegister("anc_3", sq.StateStorageType.Boolean, 1)(state)
    anc_2 = sq.AddRegister("anc_2", sq.StateStorageType.Boolean, 1)(state)
    anc_1 = sq.AddRegister("anc_1", sq.StateStorageType.Boolean, 1)(state)

    sq.State_Prep_via_QRAM(qram_b, "main_reg", data_size, rational_size)(state)

    return np.array([])
