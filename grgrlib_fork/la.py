#!/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import scipy.linalg as sl
import matplotlib.pyplot as plt
from numba import njit


def givens_rotation(a, b):
    """Compute matrix entries for Givens rotation."""
    r = np.hypot(a, b)
    c = a/r
    s = -b/r

    return (c, s)


@njit(cache=True, nogil=True, fastmath=True)
def householder_reflection(x):
    alpha = x[0]
    s = np.linalg.norm(x[1:])**2
    v = x.copy()

    if s == 0:
        tau = 0.
    else:
        t = np.sqrt(alpha**2 + s)
        v[0] = alpha - t if alpha <= 0 else -s / (alpha + t)

        tau = 2 * v[0]**2 / (s + v[0]**2)
        v /= v[0]

    return v, tau


@njit(cache=True, nogil=True, fastmath=True)
def householder_reflection_right(x):
    alpha = x[-1]
    s = np.linalg.norm(x[:-1])**2
    v = x.copy()

    if s == 0:
        tau = 0.
    else:
        t = np.sqrt(alpha**2 + s)
        v[-1] = alpha - t if alpha <= 0 else -s / (alpha + t)

        tau = 2 * v[-1]**2 / (s + v[-1]**2)
        v /= v[-1]

    return v, tau


def qr_gr(A):
    """Perform QR decomposition of matrix A using Givens rotation."""
    num_rows, num_cols = np.shape(A)

    # Initialize orthogonal matrix Q and upper triangular matrix R.
    Q = np.identity(num_rows)
    R = np.copy(A)

    # Iterate over lower triangular matrix.
    (rows, cols) = np.tril_indices(num_rows, -1, num_cols)
    for (row, col) in zip(rows, cols):

        # Compute Givens rotation matrix and
        # zero-out lower triangular matrix entries.
        if R[row, col] != 0:
            (c, s) = givens_rotation(R[col, col], R[row, col])

            G = np.identity(num_rows)
            G[[col, row], [col, row]] = c
            G[row, col] = s
            G[col, row] = -s

            R = np.dot(G, R)
            Q = np.dot(Q, G.T)

    return (Q, R)


def qr_hh(A):
    """Perform QR decomposition of matrix A using Householder reflections.
    """

    M = A.copy()
    m, n = M.shape
    Q = np.eye(m)

    for i in range(min(m, n)):

        a = M[i:, i]

        v, tau = householder_reflection(a)

        H = np.identity(m-i)
        H -= tau * np.outer(v, v)

        M[i:] = H @ M[i:]
        Q[:, i:] = Q[:, i:] @ H

    return Q, M


def rq_hh(A):
    """Perform RQ decomposition of matrix A using Householder reflections.
    """

    M = A.copy()
    m, n = M.shape
    Q = np.eye(n)

    for i in range(min(m, n)):

        a = M[-1-i, :n-i]

        v, tau = householder_reflection_right(a)

        H = np.identity(n-i)
        H -= tau * np.outer(v, v)

        M[:, :n-i] = M[:, :n-i] @ H
        Q[:n-i, :] = H @ Q[:n-i, :]

    return M, Q


def ql(M):
    """Perform QL decomposition of matrix A using scipy
    """
    r, q = sl.rq(M.T)
    return q.T, r.T


@njit(cache=True, nogil=True)
def shredder_basic(M, tol, verbose):

    m, n = M.shape
    Q = np.eye(m)

    j = 0

    for i in range(min(m, n)):

        while j < n:

            a = np.ascontiguousarray(Q.T[i:]) @ np.ascontiguousarray(M[:, j])
            do = False
            for ia in a:
                if abs(ia) > tol:
                    do = True
                    break

            if do:
                # apply Householder transformation
                v, tau = householder_reflection(a)

                H = np.identity(m-i)
                H -= tau * np.outer(v, v)

                Q[:, i:] = np.ascontiguousarray(Q[:, i:]) @ H

                if verbose:
                    print("...shredding row", j, "and col", i)
                break

            else:
                j += 1

    return Q


@njit(cache=True, nogil=True)
def shredder_pivoting(M, tol, verbose):
    """The DS-decomposition with pivoting"""

    m, n = M.shape
    M = M.copy().astype(np.float64)
    Q = np.eye(m)
    P = np.arange(n)

    j = 0

    for i in range(min(m, n)):

        # pivoting loop
        k = i
        while True:
            if k == n:
                break
            if np.any(np.abs(M[i:, k]) > tol):
                if k != i:
                    # move columns
                    M[:, np.array([i, k])] = M[:, np.array([k, i])]
                    P[np.array([i, k])] = P[np.array([k, i])]
                break
            k += 1

        while j < n:
            if np.any(np.abs(M[i:, j]) > tol):

                # apply Householder transformation
                a = M[i:, j]
                v, tau = householder_reflection(a)

                H = np.identity(m-i)
                H -= tau * np.outer(v, v)
                M[i:] = H @ M[i:]
                Q[:, i:] = np.ascontiguousarray(Q[:, i:]) @ H

                if verbose:
                    print("...shredding row", j, "and col", i)
                break

            else:
                j += 1

    return Q, M, P


@njit(cache=True, nogil=True)
def shredder_non_pivoting(M, tol, verbose):
    """The DS-decomposition with anti-pivoting"""

    m, n = M.shape
    M = M.copy().astype(np.float64)
    Q = np.eye(m)
    P = np.arange(n)

    j = 0

    for i in range(min(m, n)):

        # anti-pivoting
        # for each i move those columns forward that do not need transformation

        for k in range(j, n):
            if np.all(np.abs(M[i:, k]) < tol):
                # move columns
                if k != j:
                    M[:, np.array([j, k])] = M[:, np.array([k, j])]
                    P[np.array([j, k])] = P[np.array([k, j])]

                if verbose:
                    print('...switching rows', j, 'and', k)
                j += 1

        while j < n:
            if np.any(np.abs(M[i:, j]) > tol):

                # apply Householder transformation
                a = M[i:, j]
                v, tau = householder_reflection(a)

                H = np.identity(m-i)
                H -= tau * np.outer(v, v)
                M[i:] = H @ M[i:]
                Q[:, i:] = np.ascontiguousarray(Q[:, i:]) @ H

                if verbose:
                    print("...shredding row", j, "and col", i)
                break

            else:
                j += 1

    return Q, M, P


def shredder(M, pivoting=None, tol=1e-11, verbose=False):
    """The QS decomposition from "Efficient Solution of Models with Occasionally Binding Constraints" (Gregor Boehl) 

    The QS decomposition uses Householder reflections to bring a system in the row-echolon form. This is a dispatcher for the sub-functions.
    """

    if pivoting is None:
        q = shredder_basic(M, tol, verbose)
        return q, q.T @ M
    elif pivoting:
        return shredder_pivoting(M, tol, verbose)
    elif not pivoting:
        return shredder_non_pivoting(M, tol, verbose)
    else:
        raise NotImplementedError


def nearestPSD(A):

    B = (A + A.T)/2
    H = sl.polar(B)[1]

    return (B + H)/2
