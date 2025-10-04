import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

# a fix for making paths working on all OS
BASE = os.path.dirname(os.path.abspath(__file__))

# Create keys
def generate_keys():
    # Generate a private RSA key
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# encrypt plaintext file
def encrypt_file(file_path, public_key, output_path):
    # Read the plaintext data from the file
    with open(file_path, "rb") as file:
        plaintext = file.read()

    # Load the public key
    public_key = RSA.import_key(public_key)

    # Encrypt the data using OAEP padding with SHA256
    cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
    ciphertext = cipher.encrypt(plaintext)

    # Write the encrypted data to the specified output file
    with open(output_path, "wb") as file:
        file.write(ciphertext)

# decrypt ciphertext file
def decrypt_file(encrypted_file_path, private_key, output_path):
    # Read the encrypted data
    with open(encrypted_file_path, "rb") as file:
        ciphertext = file.read()

    # Load the private key
    private_key = RSA.import_key(private_key)

    # Decrypt the data using OAEP padding with SHA256
    cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
    plaintext = cipher.decrypt(ciphertext)

    # Write the decrypted data back to the specified output file
    with open(output_path, "wb") as file:
        file.write(plaintext)

def main():
    # Generate RSA keys
    private_key, public_key = generate_keys()

    # Define file paths using BASE for relative paths
    file_path = os.path.join(BASE, "in", "sensitive.txt")
    encrypted_file_path = os.path.join(BASE, "out", "sensitive_enc")
    decrypted_file_path = os.path.join(BASE,  "out", "sensitive_dec")

    # Encrypt and decrypt the file
    encrypt_file(file_path, public_key, encrypted_file_path)
    decrypt_file(encrypted_file_path, private_key, decrypted_file_path)
    print("CHECK INSIDE out FOLDER")

if __name__ == "__main__":
    main()
