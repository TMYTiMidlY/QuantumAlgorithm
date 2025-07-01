from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np
import pysparq as sq
from numpy.typing import NDArray

from .. import utils
from .fundamental import (
    QDADebugger,
    compute_step_rate,
    get_fidelity,
    make_vector_tree,
    scale_and_convert_vector,
)


class Walk_s_via_QRAM_Debug:
    def __init__(
        self,
        qram_A,
        qram_b,
        matrix_A,
        vector_b,
        main_reg,
        anc_UA,
        anc_1,
        anc_2,
        anc_3,
        anc_4,
        s,
        kappa,
        p,
        data_size,
        rational_size,
    ):
        self.walk = sq.Walk_s_via_QRAM(
            qram_A,
            qram_b,
            main_reg,
            anc_UA,
            anc_1,
            anc_2,
            anc_3,
            anc_4,
            s,
            kappa,
            p,
            data_size,
            rational_size,
        )
        self.debugger = QDADebugger(matrix_A, vector_b, s, kappa, p)

    def __call__(self, state: sq.SparseState):
        self.walk(state)

    def dag(self, state: sq.SparseState):
        self.walk.dag(state)

    def get_mid_eigenstate(self):
        return self.debugger.get_mid_eigenstate()


@dataclass
class WalkSequence_via_QRAM_Debug:
    qram_A: sq.QRAMCircuit_qutrit
    qram_b: sq.QRAMCircuit_qutrit
    matrix_A: NDArray[np.float64]
    vector_b: NDArray[np.float64]
    main_reg: str
    anc_UA: str
    anc_1: str
    anc_2: str
    anc_3: str
    anc_4: str
    steps: int
    kappa: float
    p: float
    data_size: int
    rational_size: int

    def __call__(self, state):
        for n in range(self.steps):
            s = n / self.steps
            walk = Walk_s_via_QRAM_Debug(
                self.qram_A,
                self.qram_b,
                self.matrix_A,
                self.vector_b,
                self.main_reg,
                self.anc_UA,
                self.anc_1,
                self.anc_2,
                self.anc_3,
                self.anc_4,
                s,
                self.kappa,
                self.p,
                self.data_size,
                self.rational_size,
            )
            walk(state)
            sq.ClearZero()(state)

            if (n + 1) % 2 == 0:
                mid_state, p_success = sq.PartialTraceSelect(
                    {self.anc_UA: 0, self.anc_2: 0, self.anc_3: 0}
                ).get_projected_full(state)
                mid_state = np.array(mid_state, dtype=np.complex128).real
                ideal_state = walk.get_mid_eigenstate()
                fidelity = get_fidelity(ideal_state, mid_state)

                print(
                    f"step: {n} / {self.steps}, fidelity: {fidelity}, p_success: {p_success}"
                )
                print(f"Maximum Qubit Count = {sq.System.max_qubit_count}")
                print(f"Maximum Register Count = {sq.System.max_register_count}")
                print(f"Maximum System Size = {sq.System.max_system_size}")
                print("")

    def dag(self, state):
        for n in range(self.steps):
            if (n + 1) % 10 == 0:
                print(f"step: {n}")
            s = (self.steps - n - 1) / self.steps
            walk = Walk_s_via_QRAM_Debug(
                self.qram_A,
                self.qram_b,
                self.matrix_A,
                self.vector_b,
                self.main_reg,
                self.anc_UA,
                self.anc_1,
                self.anc_2,
                self.anc_3,
                self.anc_4,
                s,
                self.kappa,
                self.p,
                self.data_size,
                self.rational_size,
            )
            walk.dag(state)

            sq.ClearZero()(state)


def classical2quantum(
    A_c: np.ndarray | list, b_c: np.ndarray | list
) -> tuple[
    NDArray[np.float64], NDArray[np.float64], Callable[[np.ndarray], np.ndarray]
]:
    """
    Convert a classical linear system Ax = b to quantum-compatible form

    Returns:
        A_q: Quantum-compatible matrix (Hermitian, power-of-2 dimension)
        b_q: Corresponding right-hand side vector
        recover_x: Function to recover original solution from quantum solution
    """
    A_c = np.array(A_c, dtype=np.float64)
    b_c = np.array(b_c, dtype=np.float64)

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
        # print("Input A is already Hermitian.")
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
        # print("Dimension is already a power of 2.")
        A_q = A_herm
        b_q = b_herm
    else:
        print(f"Padding dimension from {herm_dim} to {padded_dim}")
        A_q = np.identity(padded_dim, dtype=A_herm.dtype)
        b_q = np.zeros(padded_dim, dtype=b_herm.dtype)

        A_q[:herm_dim, :herm_dim] = A_herm
        b_q[:herm_dim] = b_herm

    # Step 3: Normalize the matrix A_q and vector b_q
    b_q /= np.linalg.norm(b_q)
    A_q /= np.linalg.norm(A_q)

    # Step 4: Create the recovery function
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

    return np.array(A_q, dtype=np.float64), np.array(b_q, dtype=np.float64), recover_x


def solve(
    A: np.ndarray,
    b: np.ndarray,
    kappa: Optional[float] = None,
    p: float = 1.3,
    step_rate: float = 0.01,
) -> np.ndarray:
    A = np.array(A, dtype=np.float64)
    b = np.array(b, dtype=np.float64)

    if kappa is None:
        kappa = utils.condest(A)
    print(f"{kappa = }")

    steps = compute_step_rate(step_rate, kappa)
    print(f"{steps = }")

    A, b, recover_x = classical2quantum(A, b)

    data_size = 50
    rational_size = 51

    exponent = 15
    log_column_size = int(np.ceil(np.log2(A.shape[0])))
    if A.shape[0] != 2**log_column_size:
        raise ValueError(
            "Matrix dimension is not a power of 2. Call 'classical2quantum' first."
        )

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
    WalkSequence_via_QRAM_Debug(
        qram_A,
        qram_b,
        A,
        b,
        "main_reg",
        "anc_UA",
        "anc_1",
        "anc_2",
        "anc_3",
        "anc_4",
        steps,
        kappa,
        p,
        data_size,
        rational_size,
    )(state)

    # Calculate the total probability of the subspace where anc_UA, anc_2, anc_3 are 0
    prob_inv0 = sq.PartialTraceSelect({anc_UA: 0, anc_2: 0, anc_3: 0})(state)
    prob0 = (1.0 / prob_inv0) ** 2

    print("Success probability after walk sequence:", prob0)

    sol, _ = sq.PartialTraceSelect(
        {anc_UA: 0, anc_1: 1, anc_2: 0, anc_3: 0, anc_4: 0}
    ).get_projected_full(state)
    sol = np.array(sol, np.complex128)
    sol = recover_x(sol.real)

    return sol
