# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about plotting and basic data types needed in numpy/scipy.

Teaching focus
  - np.array
  - CubicSpline
  - plot

NumPy
  - Core Purpose: NumPy is the foundation for numerical computations in
    Python.
  - It provides basic tools for working with arrays, performing element-wise
    mathematical operations, and leveraging efficient data storage.

SciPy
  - Core Purpose: SciPy builds on NumPy and offers additional advanced
    numerical computing functionality.
  - It is designed for more specialized tasks like optimization, statistics,
    advanced linear algebra, signal processing, and more.

Content
  - scipy.stats: Statistics, probability distributions, hypothesis testing
  - scipy.optimize: Solvers for root-finding, curve fitting, minimization
  - scipy.integrate: Numerical integration (quad, odeint)
  - scipy.interpolate: Interpolation for missing data, or function approximation
  - scipy.fft: Fast Fourier Transforms
  - scipy.signal: Signal processing (filters, convolutions)
  - scipy.linalg: Linear algebra (extends numpy.linalg)
  - scipy.sparse: parse matrices and solvers
  - scipy.spatial: Spatial algorithms (KDTree, distances, Delaunay)
  - scipy.ndimage: Image processing and filtering
  - scipy.cluster: Clustering algorithms (hierarchical, k-means)

Preparations
  - virtual environment activated and libs installed, here:
        pip install scipy
"""

import numpy as np
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import CubicSpline

def basic_data_types():
    """ prepare data """
    print("\nbasic_data_types\n================")

    b = np.array([0, 1, 2])                 # vector, 1d array
    A = np.array([                          # matrix, 2d array
        [1, 2, 3],
        [0, 1, 4],
        [5, 6, 0]
    ])
    print(f" 1| {b=}\n    {A=}")

    x1d = np.linspace(0, 2, 5)              # [0,2] with 5 steps
    y1d = np.square(x1d)                    # vectorized square function
    print(f" 2| {x1d=}\n    {y1d=}")

    x2d, y2d = np.meshgrid(x1d, y1d)        # a 2D grid
    print(f" 3| {x2d=}\n    {y2d=}")


def plot_1d_data():
    """ plot 1d data """
    print("\nplot_1d_data\n============")

    # noisy measurements
    x_data = np.array([0, 1, 2, 3, 4, 5, 6])
    y_data = np.array([0.1, 0.7, 0.8, 0.05, -0.7, -1.0, -0.2])

    cs = CubicSpline(x_data, y_data)
    x_fine = np.linspace(0, 6, 300)
    y_fine = cs(x_fine)
    # first two plots
    plt.plot(x_fine, y_fine, color='blue', label='cubic spline')
    plt.plot(x_data, y_data, 'x', color='red', label='measured')

    x1d = np.linspace(0, 6, 13)
    y1d = np.sin(x1d)                       # y1d = [math.sin(x) for x in x1d]
    # third plot
    plt.plot(x1d, y1d, marker='o', linestyle='--', color='blue', label='sin-model', markerfacecolor='red', markeredgecolor='black')

    # plot properties
    plt.title("curves")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.show()                              # this can be shown in PyCharm


def plot_2d_data():
    """ plot 2d data """
    print("\nplot_data\n=========")

    def f(x, y):                            # R^2 -> R
        return np.sin(np.sqrt(x**2 + y**2))

    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)                # X,Y 2D grids
    Z = f(X, Y)                             # values on the grid

    # Contour Plot: shows curves (contour lines) that connect points with the
    # same value on the surface

    contour = plt.contourf(X, Y, Z, cmap="viridis", levels=20)
    plt.colorbar(contour)
    plt.title("Contour Plot of f(x, y) = sin(sqrt(x² + y²))")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    # no legend
    plt.show()


    # Surface Plot: a three-dimensional (3D) visualization that is used to
    # display a surface, represented by a mathematical function,
    # over a defined two-dimensional grid

    fig = plt.figure()                          # container for the plot
    ax = fig.add_subplot(111, projection='3d')  # adds subplot; the `111` specifies 1 row, 1 col., and 1st subplot
    surface = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor='k', alpha=0.8)
    fig.colorbar(surface, ax=ax, shrink=0.5, aspect=10)
    ax.set_title("Surface Plot of f(x, y) = sin(sqrt(x² + y²))")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("f(x, y)")
    plt.show()


if __name__ == '__main__':
    basic_data_types()
    plot_1d_data()
    plot_2d_data()
