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

NOTE:
- ChatGPT was used for some clarification of concepts and explanations of fast modular exponentiation.
- All code was written manually using the references above and additional research.
"""

import os
import os.path 
import primegen as pg  
# I'm importing functions from primegen.py to keep it clean(ish) below. I'm also trying to comment a bit more than usual!

#for making paths working on all OS. Adapted from COSC2536 Lecture 4 onwards
BASE=os.path.dirname(os.path.abspath(__file__))

# Generate two large primes for RSA - please see primegen.py for details and extensive comments :)

# Using 256-bit primes here for demonstration, I understand 2048-bit is recommended for real RSA. On my machine 1024 bit takes a few seconds to generate, 2048 took a minute or so :)
prime_p, prime_q = pg.generate_two_distinct_primes(256)
print("RSA primes generated:")
print("p =", prime_p)
print("q =", prime_q)

#  Compute RSA parameters
modulus_n = prime_p * prime_q                # n = p * q
totient_phi = (prime_p - 1) * (prime_q - 1) # φ(n) = (p-1)*(q-1)

# Choose a public exponent e
# Common choice: 65537 (must be coprime to φ(n))
public_exponent_e = 65537

# Verify gcd(e, φ(n)) = 1
if pg.gcd(public_exponent_e, totient_phi) != 1:
    raise ValueError("Chosen e is not coprime to φ(n). Choose a different e.")

# Compute private exponent d, the modular inverse of e mod φ(n)
private_exponent_d = pg.mod_inverse(public_exponent_e, totient_phi)

print("\nRSA key parameters:")
print("n =", modulus_n)
print("φ(n) =", totient_phi)
print("Public exponent e =", public_exponent_e)
print("Private exponent d =", private_exponent_d)

#  Encrypt student number
student_number = 4101575
ciphertext = pg.modular_exponentiation(student_number, public_exponent_e, modulus_n)

# Save ciphertext to output file
ciphertext_file_path = os.path.join(BASE, "output", "student_number_encrypted.txt")
os.makedirs(os.path.dirname(ciphertext_file_path), exist_ok=True)
with open(ciphertext_file_path, "w") as f:
    f.write(str(ciphertext))
print("\nCiphertext saved to:", ciphertext_file_path)
print("Ciphertext:", ciphertext)

#  Decrypt ciphertext 
decrypted_message = pg.modular_exponentiation(ciphertext, private_exponent_d, modulus_n)

# Save decrypted message to output file
decrypted_file_path = os.path.join(BASE, "output", "student_number_decrypted.txt")
with open(decrypted_file_path, "w") as f:
    f.write(str(decrypted_message))
print("\nDecrypted message saved to:", decrypted_file_path)
print("Decrypted message:", decrypted_message)

#  Verify correctness
if decrypted_message == student_number:
    print("***Decrypted message matches original student number.***")
else:
    print("Error! Decrypted message does not match original.")