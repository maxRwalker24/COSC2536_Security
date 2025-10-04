"""
task4-hybrid.py
Hybrid encryption of a file using AES (symmetric) and RSA (asymmetric with OAEP padding)
References: 
- Lecture 7, hybrid_crypto.py
- Lecture 6, rsa_with_signature.py
Other sources:
- Cryptography.io documentation: https://cryptography.io/en/latest/

This program encrypts and decrypts 'task2.txt' using hybrid encryption.
AES is used to encrypt the file content, and RSA encrypts the AES key securely.
All RSA keys, encrypted data, and decrypted data are saved to files.
"""

import os
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes, padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


# BASE variable for cross-platform paths
# Process adapted from sample code as per COSC2536 Lecture 4 onwards
BASE = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(BASE, "input")
KEYS_FOLDER = os.path.join(BASE, "keys")
OUTPUT_FOLDER = os.path.join(BASE, "output")


def generate_rsa_keys():
    """
    Generate RSA private and public keys.
    Based on Lecture 7 hybrid_crypto.py, function generate_rsa_keys().
    - RSA key size: 2048 bits (secure, standard)
    - Public exponent: 65537 (common choice for RSA)
    Returns:
        private_key, public_key (cryptography objects)
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def save_rsa_keys(private_key, public_key):
    """
    Save RSA private and public keys to PEM files in the keys/ folder.
    
    References:
    - Lecture 6: rsa_with_signature.py demonstrated serialization of RSA keys using PKCS8 for private key and SubjectPublicKeyInfo for public key.
    - Lecture 7: hybrid_crypto.py uses similar key handling for hybrid encryption.
    
    Notes:
    - Private key saved unencrypted (NoEncryption) for demonstration.
    - Public key saved in standard SubjectPublicKeyInfo format.
    
    Returns:
        private_path, public_path (full file paths) ffor display
    """
    private_path = os.path.join(KEYS_FOLDER, "rsa_private_key.pem")
    public_path = os.path.join(KEYS_FOLDER, "rsa_public_key.pem")
    
    # Serialize and save private key (Lecture 6)
    # PKCS8 is a standard format for storing private keys (RSA, EC, etc.).
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,  # Lecture 6 style
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(private_path, "wb") as f:
        f.write(private_key_pem)
    
    # Serialize and save public key (Lecture 6)
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(public_path, "wb") as f:
        f.write(public_key_pem)
    
    return private_path, public_path


def encrypt_file(file_path, public_key):
    """
    Hybrid encryption of a file:
    - AES (symmetric) encrypts the file content
      - AES-256 key generated randomly
      - CFB mode used for streaming encryption
      - PKCS7 padding applied to plaintext (Lecture 7)
    - RSA (asymmetric) encrypts the AES key using OAEP padding
      - OAEP with MGF1 and SHA-256 ensures padding security (prevents textbook RSA attacks)
    Returns:
        encrypted_message, iv, encrypted_key
    """
    # Read the plaintext file
    with open(file_path, "r") as f:
        message = f.read()
    
    # Generate AES-256 symmetric key
    symmetric_key = os.urandom(32)
    iv = os.urandom(16)  # AES initialization vector
    
    # AES encryption (Lecture 7 example)
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Apply PKCS7 padding (Lecture 7, hybrid_crypto.py)
    # PKCS7 is a padding standard used when encrypting data with block ciphers (like AES).
    padder = sym_padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    
    encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
    
    # Encrypt AES key using RSA public key with OAEP (Lecture 7)
    encrypted_key = public_key.encrypt(
        symmetric_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return encrypted_message, iv, encrypted_key

def decrypt_file(encrypted_message, iv, encrypted_key, private_key):
    """
    Based on Lecture 7 hybrid_crypto.py, function decrypt_message().
    Hybrid decryption of a file:
    - RSA decrypts the AES symmetric key using private key (OAEP padding)
    - AES decrypts the content using the recovered symmetric key
    - PKCS7 unpadding applied to recover original plaintext
    Returns:
        decrypted_message (str)
    """
    # Decrypt symmetric AES key using RSA private key
    symmetric_key = private_key.decrypt(
        encrypted_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # AES decryption
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(encrypted_message) + decryptor.finalize()
    
    # Remove PKCS7 padding to get original message
    unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_message = unpadder.update(padded_message) + unpadder.finalize()
    
    return decrypted_message.decode()


# Main Execution / Driver Code

if __name__ == "__main__":
    # Generate RSA keys (Lecture 7)
    private_key, public_key = generate_rsa_keys()
    
    # Save keys to files
    private_path, public_path = save_rsa_keys(private_key, public_key)
    print(f"RSA Private Key saved to: {private_path}")
    print(f"RSA Public Key saved to: {public_path}\n")
    
    # Encrypt the input file
    input_file = os.path.join(INPUT_FOLDER, "task2.txt")
    encrypted_message, iv, encrypted_key = encrypt_file(input_file, public_key)
    
    # Save encrypted file
    encrypted_file_path = os.path.join(OUTPUT_FOLDER, "task2_encrypted.txt")
    with open(encrypted_file_path, "wb") as f:
        f.write(encrypted_message)
    
    # Display all encryption outputs
    print("Encrypted Message (base64):", b64encode(encrypted_message).decode())
    print("\nInitialization Vector (IV, base64):", b64encode(iv).decode())
    print("\nEncrypted AES Key (base64):", b64encode(encrypted_key).decode(), "\n")
    
    # Decrypt the encrypted file
    decrypted_message = decrypt_file(encrypted_message, iv, encrypted_key, private_key)
    
    # Save decrypted file
    decrypted_file_path = os.path.join(OUTPUT_FOLDER, "task2_decrypted.txt")
    with open(decrypted_file_path, "w") as f:
        f.write(decrypted_message)
    
    print(f"Decrypted Message:\n{decrypted_message}\n")

    

