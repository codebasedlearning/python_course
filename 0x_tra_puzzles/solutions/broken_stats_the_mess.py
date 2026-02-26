# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Puzzle 'Broken Stats' — A messy statistics calculator with subtle bugs.

This script computes mean, variance, standard deviation, median, and mode
for a dataset. It produces output that *looks* plausible but is wrong in
several ways. Your job: find all the bugs using pair debugging.

Bugs range from classic off-by-one errors to floating-point traps.
The code also has questionable style — but the task is to fix correctness
first, then discuss what you would refactor.

Expected correct results for DATA:
  mean     = 5.0
  variance = 8.5  (sample variance, n-1)
  stddev   = 2.9154...
  median   = 4.5
  mode     = 2

How many bugs can you find?
"""


DATA = [2, 7, 3, 8, 2, 5, 1, 9, 4, 6]


# --- Bug 1: accumulator uses integer division ---

def calc_mean(numbers):
    t = 0
    for x in numbers:
        t = t + x
    return t // len(numbers)        # BUG: should be / not //


# --- Bug 2: variance uses n instead of n-1 (population vs sample) ---

def calc_variance(numbers):
    m = calc_mean(numbers)
    s = 0.0
    for x in numbers:
        s += (x - m) * (x - m)
    return s / len(numbers)         # BUG: should be len(numbers) - 1 for sample variance


# --- Bug 3: sqrt via Newton's method has wrong convergence check ---

def my_sqrt(value):
    if value < 0:
        return -1               # BUG: should raise or return NaN, not -1
    if value == 0:
        return 0
    guess = value / 2.0
    for _ in range(100):
        new_guess = (guess + value / guess) / 2.0
        if abs(new_guess - guess) < 0.1:   # BUG: tolerance way too large
            break
        guess = new_guess
    return round(guess, 2)                  # BUG: rounding hides precision


def calc_stddev(numbers):
    return my_sqrt(calc_variance(numbers))


# --- Bug 4: median sort modifies original + wrong index for even length ---

def calc_median(numbers):
    numbers.sort()                          # BUG: modifies the original list
    n = len(numbers)
    if n % 2 == 1:
        return numbers[n // 2]
    else:
        mid = n // 2
        return (numbers[mid] + numbers[mid + 1]) / 2   # BUG: should be mid-1 and mid


# --- Bug 5: mode counts are compared wrong ---

def calc_mode(numbers):
    counts = {}
    for x in numbers:
        if x in counts:
            counts[x] = counts[x] + 1
        else:
            counts[x] = 0                  # BUG: first occurrence should be 1, not 0
    best = None
    best_count = 0
    for val, cnt in counts.items():
        if cnt > best_count:                # BUG: >= would handle ties, but the real
            best_count = cnt                #       issue is the off-by-one in counts
            best = val
    return best


# --- Messy main that chains the bugs ---

def main():
    d = DATA
    print(f"data:     {d}")

    m = calc_mean(d)
    print(f"mean:     {m}")

    v = calc_variance(d)
    print(f"variance: {v}")

    sd = calc_stddev(d)
    print(f"stddev:   {sd}")

    # NOTE: calc_median mutates d, so order matters
    med = calc_median(d)
    print(f"median:   {med}")

    mo = calc_mode(d)
    print(f"mode:     {mo}")

    # "validation" that looks convincing but is wrong
    total_check = sum(DATA) / len(DATA)
    print(f"\ncheck mean: {total_check} (via sum/len)")
    print(f"match? {'yes' if total_check == m else 'NO — something is off'}")


if __name__ == "__main__":
    main()
