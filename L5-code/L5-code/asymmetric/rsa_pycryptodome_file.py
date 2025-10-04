# Make sure that you have installed pycryptodome
# pip install pycryptodome

# Reference: code borrows from official documentation
# https://www.pycryptodome.org

# Import necessary modules from pycryptodome
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os

# Establish a base path to make paths work on all OS
BASE = os.path.dirname(os.path.abspath(__file__))

# Generate new RSA key
def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    # Ensure the directory exists before saving files
    os.makedirs(os.path.join(BASE, "keys"), exist_ok=True)
    # Save private key
    with open(os.path.join(BASE, "keys", "private.cryptodome.pem"), "wb") as pr:
        pr.write(private_key)
    # Save public key
    with open(os.path.join(BASE, "keys", "public.cryptodome.pem"), "wb") as pu:
        pu.write(public_key)

def encrypt_file(file_path, public_key_path, encrypted_file_path):
    # Import the public key
    with open(os.path.join(BASE, public_key_path), "rb") as f:
        public_key = RSA.import_key(f.read())
    # Read the file to encrypt
    with open(os.path.join(BASE, file_path), "rb") as f:
        data = f.read()
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher.encrypt(data)
    # Write the encrypted data
    with open(os.path.join(BASE, encrypted_file_path), "wb") as f:
        f.write(encrypted_data)

def decrypt_file(encrypted_file_path, private_key_path, decrypted_file_path):
    # Import the private key
    with open(os.path.join(BASE, private_key_path), "rb") as f:
        private_key = RSA.import_key(f.read())
    # Read the encrypted file
    with open(os.path.join(BASE, encrypted_file_path), "rb") as f:
        encrypted_data = f.read()
    cipher = PKCS1_OAEP.new(private_key)
    data = cipher.decrypt(encrypted_data)
    # Write the decrypted data
    with open(os.path.join(BASE, decrypted_file_path), "wb") as f:
        f.write(data)

if __name__ == "__main__":
    generate_keys()  # Generate keys and save to files
    encrypt_file("in/sensitive.txt", "keys/public.cryptodome.pem", "out/sensitive_cryptodome_enc")  # Encrypt the file and specify output path
    decrypt_file("out/sensitive_cryptodome_enc", "keys/private.cryptodome.pem", "out/sensitive_cryptodome_dec")  # Decrypt the file and specify output path
