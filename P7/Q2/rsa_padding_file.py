import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# a fix for making paths working on all OS
BASE = os.path.dirname(os.path.abspath(__file__))

# Create keys
def generate_keys():
    # Generate a private RSA key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    # Derive the public key from the private key
    public_key = private_key.public_key()
    return private_key, public_key

# encrypt plaintext file
def encrypt_file(file_path, public_key, output_path):
    # Read the plaintext data from the file
    with open(file_path, "rb") as file:
        plaintext = file.read()

    # Encrypt the data using OAEP padding 
    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Write the encrypted data to the specified output file
    with open(output_path, "wb") as file:
        file.write(ciphertext)

# decrypt ciphertext file
def decrypt_file(encrypted_file_path, private_key, output_path):
    # Read the encrypted data
    with open(encrypted_file_path, "rb") as file:
        ciphertext = file.read()

    # Decrypt the data using OAEP padding
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

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


'''

RATIONALE:

Textbook RSA

- takes a plaintext message m, a public key (e,n) 
- (that's usually not kept secret) and 
- creates a ciphertext c = m^e mod n and 
- can be decrypted with the secret key (d) via m = c^d mod n 

This may leak information. 

For example, if you were using textbook RSA to send a simple 
message that's one of a few options  (e.g., it's a yes/no message 
or an order to buy X shares of a stock), an attacker could just encrypt
all the likely messages with public key and see which 
one exactly matches the true ciphertext.


'''
