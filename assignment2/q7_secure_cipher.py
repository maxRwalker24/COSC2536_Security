"""
secure_cipher.py
Q7.3 - Generate ciphertext that Hack.exe cannot break
Uses RSA with OAEP padding (secure) instead of textbook RSA.
Produces key.txt and cipher.txt in the BASE folder.

References:
- Lecture 7: hybrid_crypto.py (OAEP padding example)
- Cryptography.io documentation: https://cryptography.io/en/latest/

This program generates a secure RSA key pair and encrypts a plaintext message using OAEP.
Key.txt contains the public key, cipher.txt contains the encrypted message (base64-encoded).
"""

import os
from base64 import b64encode
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# BASE variable for cross-platform paths
BASE = os.path.dirname(os.path.abspath(__file__))
KEYS_FOLDER = os.path.join(BASE, "keys")
OUTPUT_FOLDER = os.path.join(BASE, "output")

#  RSA Key Generation
def generate_keys():
    """
    Generate RSA private and public keys.
    - Key size: 2048 bits (secure standard)
    - Public exponent: 65537 (common choice for RSA)
    
    Returns:
        private_key, public_key (cryptography objects)
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Save Public Key
def save_public_key(public_key, path):
    """
    Save RSA public key to a PEM file.

    References:
    - Lecture 7: hybrid_crypto.py demonstrated public key serialization.
    
    Args:
        public_key: RSA public key object
        path: destination file path
    """
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(path, "wb") as f:
        f.write(pem)

# Encrypt Message
def encrypt_message(message, public_key):
    """
    Encrypt a plaintext message using RSA with OAEP padding.
    - OAEP prevents textbook RSA attacks and ensures semantic security.
    - Uses SHA-256 for hashing and MGF1 mask generation.
    
    Args:
        message (str): plaintext to encrypt
        public_key: RSA public key object

    Returns:
        bytes: base64-encoded ciphertext
    """
    ciphertext = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return b64encode(ciphertext)

# Main Execution
if __name__ == "__main__":
    # Generate RSA keys
    private_key, public_key = generate_keys()
    
    # Save public key to key.txt for compatibility with Cipher.exe
    key_path = os.path.join(KEYS_FOLDER, "key.txt")
    save_public_key(public_key, key_path)
    print(f"Public key saved to {key_path}")
    
    # Define plaintext message (can be replaced with user input or file)
    # plaintext = "This ciphertext cannot be broken by Hack.exe."
    
    plaintext = input("Enter the plaintext message to encrypt: ")
    # Encrypt using RSA OAEP padding
    cipher_b64 = encrypt_message(plaintext, public_key)
    
    # Save ciphertext to cipher.txt
    cipher_path = os.path.join(OUTPUT_FOLDER, "cipher.txt")
    with open(cipher_path, "wb") as f:
        f.write(cipher_b64)
    print(f"Ciphertext saved to {cipher_path}")
    
    # Display encryption results
    print("\nEncryption complete. Ciphertext (base64):")
    print(cipher_b64.decode())
