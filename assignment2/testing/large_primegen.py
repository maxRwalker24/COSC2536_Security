# from sympy import prevprime, nextprime

# # Replace this with your concatenated ID
# concatenated_id = 4101575

# # Find immediate primes
# prime_below = prevprime(concatenated_id)
# prime_above = nextprime(concatenated_id)

# # Calculate distances
# distance_below = concatenated_id - prime_below
# distance_above = prime_above - concatenated_id

# # Print results
# print(f"Concatenated ID: {concatenated_id}")
# print(f"Prime below: {prime_below} (distance: {distance_below})")
# print(f"Prime above: {prime_above} (distance: {distance_above})")

from sympy import isprime

n = 4101575
range_width = 10000

print(f"Primes around {n} (±{range_width}):")
for i in range(n - range_width, n + range_width + 1):
    if isprime(i):
        print(i)

"""



1000003
999004247
"""