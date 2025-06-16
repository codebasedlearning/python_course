# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet shows a use case from scipy.linalg.

Teaching focus
  - scipy.linalg
  - solve
  - inv
  - @ operator
  - transpose
"""

from scipy.linalg import solve, inv
import numpy as np


def lin_solve():
    """ solve linear equations """
    print("\nlin_solve\n==============")

    A = np.array([
        [2, 1, -1],
        [-3, -1, 2],
        [-2, 1, 2]
    ])
    b = np.array([8, -11, -3])
    x = solve(A, b)                         # solve Ax = b

    # `@` operator was introduced in Python 3.5 instead of np.matmul(A, B)
    bs = A @ x                              # test

    print(f" 1| {A=}, {b=}, {x=}\n    -> {bs-b=}")

    A_inv = inv(A)                          # inverse
    xs = A_inv @ b                          # do not do this in real life!
    print(f" 2| {A_inv}\n    -> {np.round(xs-x,3)=} ")

    ATA = A.T                               # transpose
    print(f" 3| {A=}\n    {ATA=}")


if __name__ == '__main__':
    lin_solve()
