# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet demonstrates basic statistics with scipy.

Teaching focus
  - scipy.stats normal distribution
  - paired t-test (ttest_rel)
  - matplotlib plotting
"""

from pathlib import Path
import time
import textwrap

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import ttest_rel

from utils import print_function_header


@print_function_header
def plot_normal_distribution():
    """ plot standard normal distribution PDF """

    # Define range for x-axis
    x = np.linspace(-4, 4, 1000)

    # Get PDF values from scipy
    pdf = norm.pdf(x, loc=0, scale=1)

    # Plot
    plt.plot(x, pdf, label="Standard Normal PDF")
    plt.title("Normal Distribution (mean=0, std=1)")
    plt.xlabel("x")
    plt.ylabel("Probability Density")
    plt.grid(True)
    plt.legend()
    plt.show()

@print_function_header
def paired_t_test():
    """ paired t-test for caffeine effect on reaction times """

    before = [250, 270, 260, 300, 280, 275, 290, 265, 285, 295]
    after = [240, 250, 245, 280, 260, 255, 270, 250, 265, 275]

    # Paired t-test
    t_stat, p_value = ttest_rel(before, after)

    print(f" 1| T-statistic: {t_stat:.3f}")
    print(f" 2| P-value: {p_value:.4f}")

    if p_value < 0.05:
        print(" 3| Statistically significant: caffeine likely had an effect.")
    else:
        print(" 3| Not statistically significant: no clear evidence of caffeine effect.")

    plt.boxplot([before, after], labels=["Before Coffee", "After Coffee"])
    plt.ylabel("Reaction Time (ms)")
    plt.title("Reaction Times Before and After Caffeine")
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    plot_normal_distribution()
    paired_t_test()
