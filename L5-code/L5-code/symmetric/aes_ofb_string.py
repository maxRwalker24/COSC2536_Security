# make sure pycryptodome is installed
# WINDOWS: pip install pycryptodome 
# MAC: pip3 install pycryptodome

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def encrypt_decrypt_ofb_mode(data):
    key = get_random_bytes(16)  # AES key must be either 16, 24, or 32 bytes long
    iv = get_random_bytes(16)  # Initialization vector

    # Encrypt
    cipher_encrypt = AES.new(key, AES.MODE_OFB, iv)
    encrypted_data = cipher_encrypt.encrypt(data.encode())

    # Decrypt
    cipher_decrypt = AES.new(key, AES.MODE_OFB, iv)
    decrypted_data = cipher_decrypt.decrypt(encrypted_data).decode()

    return key, iv, encrypted_data, decrypted_data

# Example usage:
data = "Security in Computing & IT"
key, iv, encrypted_data, decrypted_data = encrypt_decrypt_ofb_mode(data)

print("Key:", key)
print("IV:", iv)
print("Encrypted Data:", encrypted_data)
print("Decrypted Data:", decrypted_data)

# OFB (short for output feedback) is an AES block cipher mode similar to the CFB mode. 
# What mainly differs from CFB is that the OFB mode relies on XOR-ing 
# plaintext and ciphertext blocks with expanded versions of the initialization vector.
# In this mode, it will encrypt the IV in the first time and encrypt the per-result. 
# Then it will use the encryption results to xor the plaintext to get ciphertext. 
