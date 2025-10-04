# make sure you have installed cryptography library
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import os.path

# For making paths work on all OS
BASE = os.path.dirname(os.path.abspath(__file__))

def encrypt_image(input_path, output_path, key):
    # Read the image file
    with open(os.path.join(BASE, input_path), "rb") as file:
        original_data = file.read()

    # Generate a random nonce, serves as the counter
    nonce = os.urandom(16)

    # Create a Cipher object using the key and nonce
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the data
    encrypted_data = encryptor.update(original_data) + encryptor.finalize()

    # Write the nonce and the encrypted data to the output file
    with open(os.path.join(BASE, output_path), "wb") as file:
        file.write(nonce + encrypted_data)

    print("File encrypted successfully.")

def decrypt_image(input_path, output_path, key):
    # Read the encrypted file
    with open(os.path.join(BASE, input_path), "rb") as file:
        file_content = file.read()

    # Extract nonce and encrypted data
    nonce = file_content[:16]
    encrypted_data = file_content[16:]

    # Create a Cipher object using the key and nonce
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Write the decrypted data to the output file
    with open(os.path.join(BASE, output_path), "wb") as file:
        file.write(decrypted_data)

    print("File decrypted successfully.")

# Generate a random AES key (AES-256)
key = os.urandom(32)  # 32 bytes for AES-256

# Specify the input and output image paths for encryption and decryption
input_image_path = 'in/troll.jpg'
encrypted_image_path = 'out/troll_encrypted.jpg'
decrypted_image_path = 'out/troll_decrypted.jpg'

# Encrypt the image
print('─' * 10)
encrypt_image(input_image_path, encrypted_image_path, key)

# prints a line separator
print('─' * 10)

# Decrypt the image
decrypt_image(encrypted_image_path, decrypted_image_path, key)
