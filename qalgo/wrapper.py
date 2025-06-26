"""
Temporary wrapper module for PySparQ type dispatch.

This module provides wrapper classes and functions that automatically dispatch
to the appropriate typed implementations in the pysparq library based on NumPy
data types.

TODO: These wrapper implementations are temporary and will be moved into the
main pysparq library as part of the internal API. Once integrated, this
wrapper.py file can be deprecated.
"""

import numpy as np

import pysparq as sq


class DenseMatrix:
    def __new__(
        cls,
        matrix: np.ndarray,
    ):
        match matrix.dtype:
            case np.integer:
                return sq.DenseMatrix_float64(matrix.astype(np.float64))
            case np.float64:
                return sq.DenseMatrix_float64(matrix)
            case np.complex128:
                return sq.DenseMatrix_complex128(matrix)
            case _:
                raise TypeError(
                    "Unsupported dtype. Use np.integer, np.float64 or np.complex128."
                )


class DenseVector:
    def __new__(cls, vector: np.ndarray):
        match vector.dtype:
            case np.integer:
                return sq.DenseMatrix_float64(vector.astype(np.float64))
            case np.float64:
                return sq.DenseVector_float64(vector)
            case np.complex128:
                return sq.DenseVector_complex128(vector)
            case _:
                raise TypeError(
                    "Unsupported dtype. Use np.integer, np.float64 or np.complex128."
                )


