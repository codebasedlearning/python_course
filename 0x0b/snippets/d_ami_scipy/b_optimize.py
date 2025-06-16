# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet shows a use case from scipy.optimize.

Teaching focus
  - scipy.optimize
  - newton
"""

from scipy.optimize import newton
import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return x ** 3 - 2 * x - 4               # roots: 2, -1+i, -1-i

def f_prime(x):
    return 3 * x ** 2 - 2

def newtons_method():
    """ solve it with Newton's method """
    print("\nnewtons_method\n==============")

    root = newton(f, x0=2.0, fprime=f_prime)
    # np.float64: guaranteed to be consistently a 64-bit floating-point number across all platforms
    print(f" 1| {root=}, {float(root)=}, f'(x) = {f(root):.5e}")

    x = np.linspace(-3, 3, 400)
    y = f(x)

    plt.plot(x, y, label='f(x) = x³ - 2x - 4')
    # x-axis
    plt.axhline(0, color='black', linewidth=0.5)
    # root as a point
    plt.scatter([root], [f(root)], color='red', label='Root')
    plt.title("Newton's Method")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    newtons_method()
