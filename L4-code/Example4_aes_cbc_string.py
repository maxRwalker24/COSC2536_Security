# THIS IS NOT THE BEST APPROACH
# WE NEED TO LEARN BASICS FIRST AND THEN MORE ADVANCED
# YOU WILL LEARN MORE ELEGANT APPROACH IN LECTORIAL 5

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
import base64

# encrypt

def encrypt(plaintext, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    padder = PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    encodedciphertext = base64.b64encode(ciphertext)
    return encodedciphertext

# decrypt

def decrypt(ciphertext, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()
    decodedciphertext = base64.b64decode(ciphertext)
    padded_data = decryptor.update(decodedciphertext) + decryptor.finalize()
    unpadder = PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()
    return plaintext

key = b'\x01\x23\x45\x67\x89\xAB\xCD\xEF\xFE\xDC\xBA\x98\x76\x54\x32\x10' \
      b'\x01\x23\x45\x67\x89\xAB\xCD\xEF\xFE\xDC\xBA\x98\x76\x54\x32\x10'

plaintext = input("Enter the plaintext: ").encode()
enc = encrypt(plaintext, key)
print("The encrypted message is :", enc)
dec = decrypt(enc, key)
print("The decrypted message is:", dec.decode('utf-8'))


'''
 code based upon documentation websites:

 https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/ 

 https://cryptography.io/en/latest/hazmat/primitives/padding/

'''