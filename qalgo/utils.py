import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as sla


def is_hermitian(A: np.ndarray, **kargs) -> bool:
    """Check if matrix A is Hermitian (self-adjoint)"""
    return A.shape[0] == A.shape[1] and np.allclose(A, A.conj().T, **kargs)


def next_power_of_2(n: int) -> int:
    """Find the next power of 2 greater than or equal to n"""
    return 2 ** int(np.ceil(np.log2(n)))


def make_complement(data: np.int64, data_sz: int) -> np.int64:
    """
    Compute the unsigned complement representation of an integer
    within a data_sz-bit space.
    """
    if data_sz == 64 or data >= 0:
        return data
    return (1 << data_sz) + data  # Equivalent to 2**data_sz + data


def get_complement(data: np.uint64, data_sz: int) -> np.int64:
    """
    Extends the sign of the lower data_sz bits of data.
    """
    if data_sz == 0:
        return np.int64(0)
    return (data << (64 - data_sz)) >> (64 - data_sz)


def condest(A, splu_opt={}, onenormest_opt={}) -> float:
    """
    Compute an estimate of the 1-norm condition number of a sparse matrix.

    Parameters
    ----------
    A : (M, M) sparse matrix
        square matrix to be inverted
    splu_opt : dict, optional
        Additional named arguments to `splu`.
    onenormest_opt : dict, optional
        Additional named arguments to `onenormest`.

    Returns
    -------
    c : {float, inf}
        The condition number of the matrix. May be infinite.

    References
    ----------
    .. [1] Nicholas J. Higham and Francoise Tisseur (2000),
           "A Block Algorithm for Matrix 1-Norm Estimation,
           with an Application to 1-Norm Pseudospectra."
           SIAM J. Matrix Anal. Appl. Vol. 21, No. 4, pp. 1185-1201.

    .. [2] William W. Hager (1984), "Condition Estimates."
           SIAM J. Sci. Stat. Comput. Vol. 5, No. 2, pp. 311-316.

    Examples
    --------
    >>> from numpy.linalg import cond
    >>> from scipy.sparse import csc_matrix
    >>> A = csc_matrix([[1., 0., 0.], [5., 8., 2.], [0., -1., 0.]], dtype=float)
    >>> A.toarray()
    array([[ 1.,  0.,  0.],
           [ 5.,  8.,  2.],
           [ 0., -1.,  0.]])
    >>> condest(A)
    45.0
    >>> cond(A.toarray(), p=1)
    45.0
    """

    # Check the input sparse matrix.
    if A.ndim != 2:
        raise ValueError("expected the matrix to have to dimensions")
    if A.shape[0] != A.shape[1]:
        raise ValueError("expected the matrix to be square")
    if A.shape[0] == 0:
        raise ValueError("cond is not defined on empty arrays")

    A = sps.csc_array(A)
    print(
        f"Ignoring {np.sum(A.diagonal() == 0)} rows/cols with zero diagonal entries \
while estimating condition number."
    )
    nonzero_diag_indices = np.nonzero(A.diagonal())[0]
    A = A[nonzero_diag_indices, :][:, nonzero_diag_indices]

    # Get LU decomposition of the matrix.
    try:
        decomposition = sla.splu(A, **splu_opt)
    except RuntimeError:
        return np.inf

    # Function for solving the equation system (original matrix).
    def matvec(rhs):
        return decomposition.solve(rhs, trans="N")

    # Function for solving the equation system (Hermitian matrix).
    def rmatvec(rhs):
        return decomposition.solve(rhs, trans="H")

    # Create a linear operator for the matrix inverse.
    op = sla.LinearOperator(A.shape, matvec=matvec, rmatvec=rmatvec)  # type: ignore

    # Compute the 1-norm of the matrix inverse (estimate).
    nrm_inv = sla.onenormest(op, **onenormest_opt)

    # Compute the 1-norm of the matrix (estimate).
    nrm_ori = sla.onenormest(A, **onenormest_opt)

    # Compute an estimate of the condition number.
    c = nrm_ori * nrm_inv  # type: ignore

    return float(c)
