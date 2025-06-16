# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet shows a use case from scipy.integrate.

Teaching focus
  - scipy.integrate
  - quad
"""

from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return np.sin(x ** 2)

def numerical_integration():
    """ solve it numerically """
    print("\nnumerical_integration\n=====================")

    result, error = quad(f, 0, 3)           # integrate from 0 to 3
    print(f" 1| estimated integral: {result:.5f}, error: {error:.2e}")

    x = np.linspace(0, 3, 1000)
    y = f(x)

    plt.plot(x, y, label="f(x) = sin(x²)")
    plt.fill_between(x, y, alpha=0.3, label="Area ≈ quad()")
    plt.title("Numerical Integration of sin(x²)")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    numerical_integration()
