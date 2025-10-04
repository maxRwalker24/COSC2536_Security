from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode
from os import urandom

def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_message(message, public_key):
    # Generate a random symmetric key for AES
    symmetric_key = urandom(32)  # AES-256

    # Encrypt the data with AES
    iv = urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = sym_padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    encrypted_message = encryptor.update(padded_data) + encryptor.finalize()

    # Encrypt the symmetric key with RSA
    encrypted_key = public_key.encrypt(
        symmetric_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return encrypted_message, iv, encrypted_key

def decrypt_message(encrypted_message, iv, encrypted_key, private_key):
    # Decrypt the symmetric key
    symmetric_key = private_key.decrypt(
        encrypted_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Decrypt the data
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(encrypted_message) + decryptor.finalize()
    unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_message = unpadder.update(padded_message) + unpadder.finalize()

    return decrypted_message.decode()

# Generate RSA keys
private_key, public_key = generate_rsa_keys()

# Original message
message = "Security in Computing & IT"

# Encrypt the message
encrypted_message, iv, encrypted_key = encrypt_message(message, public_key)

# Decrypt the message
decrypted_message = decrypt_message(encrypted_message, iv, encrypted_key, private_key)

print("Original:", message)
print("Encrypted Message:", b64encode(encrypted_message).decode())
print("IV (Initialization Vector):", b64encode(iv).decode())
print("Encrypted Symmetric Key:", b64encode(encrypted_key).decode())
print("Decrypted:", decrypted_message)
