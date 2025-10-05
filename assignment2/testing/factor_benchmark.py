import time
import csv
from sympy import isprime, nextprime, prevprime, factorint

# ----- Configuration -----
# Base number ~ your student ID (example: 4101575)
BASE = 4101575

# Test cases: offset patterns around BASE (small, medium, large gaps)
prime_pairs = [
    (prevprime(BASE), nextprime(BASE)),                 # very close primes
    (nextprime(BASE), nextprime(BASE + 10000)),         # small gap
    (nextprime(BASE), nextprime(BASE + 1000000)),       # medium gap
    (1000003, 999004247),                               # far apart (from your test)
    (prevprime(BASE**2), nextprime(BASE**2))            # large modulus test
]

# ----- Factorization Methods -----
def trial_division(n, limit=2000000):
    for i in range(2, limit):
        if n % i == 0:
            return i
    return None

def pollards_rho(n):
    if n % 2 == 0:
        return 2
    x = 2; y = 2; d = 1
    f = lambda x: (x*x + 1) % n
    while d == 1:
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)
    return None if d == n else d

def fermat_factor(n, max_iter=100000):
    a = int(n ** 0.5) + 1
    b2 = a*a - n
    count = 0
    while count < max_iter and not int(b2**0.5 + 0.5)**2 == b2:
        a += 1
        b2 = a*a - n
        count += 1
    if int(b2**0.5 + 0.5)**2 == b2:
        b = int(b2**0.5)
        return a - b
    return None

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# ----- Run Benchmarks -----
results = []

for p, q in prime_pairs:
    n = p * q
    print(f"\nTesting p={p}, q={q}")
    print(f"n={n} (bitlen={n.bit_length()})")

    row = {"p": p, "q": q, "n": n, "bits": n.bit_length()}

    # Sympy
    start = time.time()
    factors = factorint(n)
    row["sympy_time"] = round(time.time() - start, 4)
    print(" sympy:", factors, "time:", row["sympy_time"], "s")

    # Trial
    start = time.time()
    f = trial_division(n)
    row["trial_time"] = round(time.time() - start, 4)
    print(" trial:", f, "time:", row["trial_time"], "s")

    # Pollard
    start = time.time()
    f = pollards_rho(n)
    row["pollard_time"] = round(time.time() - start, 4)
    print(" pollard:", f, "time:", row["pollard_time"], "s")

    # Fermat
    start = time.time()
    f = fermat_factor(n)
    row["fermat_time"] = round(time.time() - start, 4)
    print(" fermat:", f, "time:", row["fermat_time"], "s")

    results.append(row)

# ----- Save to CSV -----
with open("factor_benchmark_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("\n✅ Results written to factor_benchmark_results.csv")
