"""
plot_factor_results.py
Visualizes factorization performance vs. prime gap using matplotlib.
"""

import csv
import matplotlib.pyplot as plt
import math

# ----- Load CSV Data -----
filename = "factor_benchmark_results.csv"  # update path if needed

prime_gaps = []
sympy_time = []
trial_time = []
pollard_time = []
fermat_time = []

with open(filename, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        p = int(row["p"])
        q = int(row["q"])
        gap = abs(q - p)
        prime_gaps.append(gap)
        sympy_time.append(float(row["sympy_time"]))
        trial_time.append(float(row["trial_time"]))
        pollard_time.append(float(row["pollard_time"]))
        fermat_time.append(float(row["fermat_time"]))

# ----- Plot Results -----
plt.figure(figsize=(8, 5))

plt.plot(prime_gaps, sympy_time, "o-", label="Sympy (factorint)")
plt.plot(prime_gaps, trial_time, "s-", label="Trial Division")
plt.plot(prime_gaps, pollard_time, "^-", label="Pollard’s Rho")
plt.plot(prime_gaps, fermat_time, "d-", label="Fermat Factorization")

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Prime Gap (|q - p|) [log scale]")
plt.ylabel("Factorization Time (s) [log scale]")
plt.title("Factorization Time vs Prime Gap Across Algorithms")
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.tight_layout()

# Optional: save to file
plt.savefig("factorization_times.png", dpi=300)
plt.show()
