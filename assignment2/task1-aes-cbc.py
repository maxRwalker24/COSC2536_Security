"""
ASSESSOR NOTE:

This decryption code is adapted from:
- COSC2536 sample AES file encryption/decryption code (COSC2536 Lecture 4+)
- Python documentation for 'binascii' module (https://docs.python.org/3/library/binascii.html)

Additional explanations:
- binascii is used to convert between hexadecimal strings and bytes, which is necessary because the encrypted file stores the ciphertext as a hex string rather than raw bytes.
- AES decryption is performed in CBC mode with PKCS7 padding.

References:
1. COSC2536 Practical 7 "aes_cbc_file.py" AES encryption/decryption sample code 
2. Python binascii module documentation: https://docs.python.org/3/library/binascii.html
3. Cryptography.io documentation: https://cryptography.io/en/latest/
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import binascii   # used to convert hex strings to bytes and vice versa
import os
import os.path

# Base directory for file paths
# Ensures file paths work on any OS - as per Lecture 4 onwards
BASE = os.path.dirname(os.path.abspath(__file__))


# Function to decrypt an AES-CBC encrypted file stored as hex
def decrypt_file(input_file_path, output_file_path, key_file_path):
    """
    Decrypts a file encrypted with AES in CBC mode, stored as hexadecimal text.
    
    Parameters:
    - input_file_path: path to the hex-encoded ciphertext file
    - output_file_path: path where the decrypted plaintext file will be saved
    - key_file_path: path to the hex-encoded AES key file
    
    Process:
    1. Read the ciphertext as a hex string and convert to bytes (binascii.unhexlify)
    2. Extract the first 16 bytes as the IV, remainder as the ciphertext
    3. Read the AES key as hex string and convert to bytes
    4. Decrypt using AES CBC mode
    5. Remove PKCS7 padding
    6. Write plaintext to output file
    """
    #  Read ciphertext stored as hex string in text file
    with open(input_file_path, 'r') as f:
        cipher_hex_string = f.read().strip()  # remove any extra whitespace

    # Convert hex string to bytes
    cipher_bytes = binascii.unhexlify(cipher_hex_string)

    #  Extract IV (first 16 bytes) and actual ciphertext
    iv = cipher_bytes[:16]
    ciphertext = cipher_bytes[16:]

    #  Read AES key from key file (hex string) and convert to bytes
    with open(key_file_path, 'r') as f:
        key_hex_string = f.read().strip()
    key_bytes = binascii.unhexlify(key_hex_string)

    #  Set up AES cipher in CBC mode and decrypt
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove PKCS7 padding to recover original plaintext
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext_bytes = unpadder.update(padded_plaintext) + unpadder.finalize()

    # Write plaintext to output file
    with open(output_file_path, 'wb') as f:
        f.write(plaintext_bytes)

    # Also print the plaintext for verification
    print("Decrypted text:\n", plaintext_bytes.decode())


# Driver code
print('─' * 10)

decrypt_file(
    BASE + '/output/q2_encrypted.txt',
    BASE + '/output/q2_decrypted.txt',
    BASE + '/keys/q2_key.txt'
)

print('─' * 10)
print("Decrypted text saved to '/output/q2_decrypted.txt'")
