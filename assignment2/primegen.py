"""
ASSESSOR NOTE:

This code is adapted from: "Python3 program Miller-Rabin primality test"
Source: https://www.geeksforgeeks.org/dsa/primality-test-set-3-miller-rabin/

Overview:
- Implements the Miller-Rabin primality test, a probabilistic algorithm
  used to check if a number is prime.
- Widely used in cryptography due to its efficiency and reliability for very large integers.

This code specifically adapts and explains:
1. Miller-Rabin primality test
   (GeeksforGeeks: https://www.geeksforgeeks.org/dsa/primality-test-set-3-miller-rabin/)
2. Fast modular exponentiation
   (CP-Algorithms: https://cp-algorithms.com/algebra/binary-exp.html)
3. Extended Euclidean Algorithm
   (Wikipedia: https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm)

References:
1. Miller-Rabin primality test (GeeksforGeeks)  
   https://www.geeksforgeeks.org/dsa/primality-test-set-3-miller-rabin/
2. Modular Exponentiation (GeeksforGeeks)  
   https://www.geeksforgeeks.org/modular-exponentiation-power-in-modular-arithmetic/
3. Miller, G.L. (1976). "Riemann’s Hypothesis and Tests for Primality".  
   Journal of Computer and System Sciences.
4. Rabin, M.O. (1980). "Probabilistic algorithm for testing primality".  
   Journal of Number Theory.

Note:
- ChatGPT was used for some clarification of concepts and explanations.
- All code was written manually using the references above and additional research.


=====================================
# NOTE
Please note that while I have adapted and learned from these sources, the code provided here is my own adaptation. I do wish to give due credit to the original authors for their work and insights!

=====================================
"""

import random

# Efficient modular exponentiation adapted from GeeksforGeeks, reference above
def modular_exponentiation(base, exponent, modulus):
    """
    Compute (base^exponent) % modulus efficiently using the square-and-multiply method.

    Rationale:
    - Direct computation of base^exponent is impractical for large exponents (e.g., 512 bits)
    - Reducing modulo 'modulus' at each step keeps numbers small
    - Exponent is expressed in binary and processed bit by bit
      For example, exponent = 13 = (1101)_2:
      base^13 = base^(8+4+1) = base^8 * base^4 * base^1
    """
    result = 1
    base = base % modulus  # initial reduction to stay within modulus
    while exponent > 0:
        if exponent & 1:  # if current bit of exponent is 1
            result = (result * base) % modulus
        exponent >>= 1     # shift exponent to process next bit
        base = (base * base) % modulus  # square base each iteration
    return result


# Single round of Miller-Rabin test
def miller_rabin_single_test(odd_factor_d, number_to_test):
    """
    Perform one probabilistic test for primality using Miller-Rabin.

    Inputs:
    - number_to_test: integer to check
    - odd_factor_d: odd factor of number_to_test-1 (so that number_to_test-1 = odd_factor_d * 2^r)

    Procedure:
    1. Randomly select a base a in [2, number_to_test-2]
    2. Compute x = a^odd_factor_d % number_to_test
    3. If x == 1 or x == number_to_test-1, number passes this round
    4. Otherwise, repeatedly square x (x = x^2 % number_to_test) and double odd_factor_d:
       - If x becomes number_to_test-1, number passes this round
       - If x becomes 1 before number_to_test-1, number is composite
    """
    random_base_a = 2 + random.randint(1, number_to_test - 4)
    x_value = modular_exponentiation(random_base_a, odd_factor_d, number_to_test)

    if x_value == 1 or x_value == number_to_test - 1:
        return True

    while odd_factor_d != number_to_test - 1:
        x_value = (x_value * x_value) % number_to_test
        odd_factor_d *= 2
        if x_value == 1:
            return False  # detected composite
        if x_value == number_to_test - 1:
            return True   # strong witness for probable primality

    return False  # definitely composite


# Full Miller-Rabin primality check
def is_probable_prime(candidate_number, number_of_rounds=40):
    """
    Check if a number is probably prime using multiple rounds of Miller-Rabin.

    Parameters:
    - candidate_number: integer to test
    - number_of_rounds: number of independent Miller-Rabin tests (higher = more confidence)

    Returns:
    - True if candidate_number is likely prime
    - False if candidate_number is composite

    Notes:
    - Any odd number > 2 can be expressed as candidate_number-1 = odd_factor_d * 2^r
    - Miller-Rabin theorem: a number passes if a^odd_factor_d ≡ 1 or a^(odd_factor_d*2^j) ≡ -1 (mod candidate_number)
    - Probability of error after number_of_rounds tests ≈ (1/4)^number_of_rounds
    """
    if candidate_number <= 1 or candidate_number == 4:
        return False
    if candidate_number <= 3:
        return True

    # Factor out powers of 2 from candidate_number-1
    odd_factor_d = candidate_number - 1
    while odd_factor_d % 2 == 0:
        odd_factor_d //= 2

    # Perform multiple independent Miller-Rabin rounds
    for _ in range(number_of_rounds):
        if not miller_rabin_single_test(odd_factor_d, candidate_number):
            return False
    return True


# Generate a single large prime
def generate_large_prime(bit_length=512):
    """
    Produce a random prime number of approximately 'bit_length' bits.

    Method:
    1. Generate random candidate of correct bit length:
       - Set MSB = 1 → ensures desired size
       - Set LSB = 1 → ensures odd number
    2. Test candidate using Miller-Rabin until prime found
    """
    while True:
        prime_candidate = random.getrandbits(bit_length) | (1 << (bit_length - 1)) | 1
        if is_probable_prime(prime_candidate, number_of_rounds=40):
            return prime_candidate


# Generate two distinct primes for RSA
def generate_two_distinct_primes(bit_length=512):
    """
    Generate two distinct large primes for RSA key generation.
    Guarantees that the primes are not equal.
    """
    prime_one = generate_large_prime(bit_length)
    prime_two = generate_large_prime(bit_length)
    while prime_two == prime_one:
        prime_two = generate_large_prime(bit_length)
    return prime_one, prime_two

# Compute private exponent d using Extended Euclidean Algorithm
def extended_gcd(a, b):
    """Return (g, x, y) such that a*x + b*y = g = gcd(a,b)"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return (g, x, y)

# Modular inverse of e mod φ(n)
def mod_inverse(e, phi):
    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % phi

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a