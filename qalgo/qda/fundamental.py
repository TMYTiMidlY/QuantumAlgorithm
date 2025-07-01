import numpy as np
from numpy.typing import NDArray
import pysparq as sq
from .. import utils
from dataclasses import dataclass


# @dataclass
# class GetOutput:
#     main_reg: str | int
#     anc_UA: str | int
#     anc_1: str | int
#     anc_2: str | int
#     anc_3: str | int
#     anc_4: str | int

#     def __post__init__(self):
#         if isinstance(self.main_reg, str):
#             self.main_reg = sq.System.get_id(self.main_reg)
#         if isinstance(self.anc_UA, str):
#             self.anc_UA = sq.System.get_id(self.anc_UA)
#         if isinstance(self.anc_1, str):
#             self.anc_1 = sq.System.get_id(self.anc_1)
#         if isinstance(self.anc_2, str):
#             self.anc_2 = sq.System.get_id(self.anc_2)
#         if isinstance(self.anc_3, str):
#             self.anc_3 = sq.System.get_id(self.anc_3)
#         if isinstance(self.anc_4, str):
#             self.anc_4 = sq.System.get_id(self.anc_4)
#         self.anc_registers = [self.anc_UA, self.anc_3, self.anc_2]

#     def __call__(self, state: list[sq.System]) -> tuple[np.ndarray, float]:
#         # The size of anc_4/anc_1 is 1. The length of state_ps is pow2(size_mreg + 1 + 1).
#         main_reg_num = sq.System.size_of(self.main_reg)
#         anc_1_num = sq.System.size_of(self.anc_1)
#         anc_4_num = sq.System.size_of(self.anc_4)
#         total_bits = main_reg_num + anc_1_num + anc_4_num
#         dim = 2**total_bits
#         state_ps = np.zeros(dim, dtype=np.complex128)

#         sum_prob = 0.0
#         for sys in state:
#             # Skip states where any ancilla register is non-zero
#             if not all(sys.get_as_uint64(reg) == 0 for reg in self.anc_registers):
#                 continue

#             # Concatenate main_reg + anc_1 + anc_4 into an index
#             bit_values = []
#             bit_values.append((sys.get_as_uint64(main_reg_num), 1))
#             bit_values.append((sys.get_as_uint64(anc_1), 1))
#             bit_values.append((sys.get_as_uint64(self.anc_4), 1))

#             idx = self.concat_value(bit_values)
#             state_ps[idx] = sys.amplitude
#             sum_prob += abs(sys.amplitude) ** 2

#         # Normalize only if necessary
#         if abs(sum_prob - 1.0) >= self.epsilon and sum_prob != 0:
#             state_ps /= np.sqrt(sum_prob)

#         return state_ps, sum_prob

#     @staticmethod
#     def concat_value(pairs: list[tuple[int, int]]) -> int:
#         """Concatenate (value, bits) pairs into a single integer index"""
#         result = 0
#         for val, bits in pairs:
#             result = (result << bits) | val
#         return result


class QDADebugger:
    def __init__(
        self,
        matrix_A: NDArray[np.float64],
        vector_b: NDArray[np.float64],
        s: float,
        kappa: float,
        p: float,
    ):
        self.matrix_A = matrix_A
        self.vector_b = vector_b
        self.row_size = len(vector_b)
        self.fs = (kappa / (kappa - 1)) * (
            1 - (1 + s * (kappa ** (p - 1) - 1)) ** (1 / (1 - p))
        )

    def get_matrix_Af(self) -> NDArray[np.float64]:
        n = self.row_size
        I = np.eye(n)
        A = self.matrix_A
        A_dag = A.T  # Hermitian transpose in real domain = transpose

        top = np.hstack([(1 - self.fs) * I, self.fs * A])
        bottom = np.hstack([self.fs * A_dag, -(1 - self.fs) * I])
        Ad = np.vstack([top, bottom])
        return Ad

    def get_vector_0b(self) -> NDArray[np.float64]:
        n = self.row_size
        return np.concatenate([self.vector_b, np.zeros(n)])

    def get_vector_1b(self) -> NDArray[np.float64]:
        n = self.row_size
        return np.concatenate([np.zeros(n), self.vector_b])

    def get_mid_eigenstate(self) -> NDArray[np.float64]:
        print(f"fs = {self.fs}")
        n = self.row_size

        if self.fs == 0:
            vec = self.get_vector_0b()
        elif self.fs == 1:
            sol = np.linalg.solve(self.matrix_A, self.vector_b)
            sol /= np.linalg.norm(sol)
            vec = np.concatenate([np.zeros(n), sol])
        elif 0 < self.fs < 1:
            Af = self.get_matrix_Af()
            b = self.get_vector_0b()
            sol = np.linalg.solve(Af, b)
            sol /= np.linalg.norm(sol)
            vec = sol
        else:
            raise RuntimeError(
                f"Invalid fs value: {self.fs}. Expected 0 <= fs <= 1."
            )

        return np.concatenate([vec, np.zeros(2 * n)], dtype=np.float64)


def compute_step_rate(step_rate: float, kappa: float) -> int:
    StepConstant = 2305
    steps = int(step_rate * StepConstant * kappa)
    if steps % 2 != 0:
        steps += 1  # Guaranteed to be an even number
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


def get_fidelity(
    state: NDArray[np.complexfloating]
    | NDArray[np.floating]
    | list[complex]
    | list[float],
    target: NDArray[np.complexfloating]
    | NDArray[np.floating]
    | list[complex]
    | list[float],
) -> float:
    if len(state) == 0:
        return 0.0
    if len(state) != len(target):
        raise RuntimeError(
            f"Error: Vectors must be of the same size! size1 = {len(state)}, size2 = {len(target)}"
        )

    sum_val = 0
    if isinstance(target[0], complex):
        for s, t in zip(state, target):
            sum_val += s * t.conjugate()
    else:
        for s, t in zip(state, target):
            sum_val += s * t

    return float(abs(sum_val))
