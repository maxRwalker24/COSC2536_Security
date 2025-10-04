# THIS IS NOT THE BEST APPROACH
# WE NEED TO LEARN BASICS FIRST AND THEN MORE ADVANCED
# YOU WILL LEARN MORE ELEGANT APPROACH IN LECTORIAL 5

from cryptography.fernet import Fernet
#salt
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os.path

# make path work with all OS
#for making paths working on all OS
BASE=os.path.dirname(os.path.abspath(__file__))

# key without salt
key = Fernet.generate_key()
print("Key: ")
print(key)

file = open(BASE + '/keys/key.key', 'wb') #wb = write bytes
file.write(key)
file.close()

# new key with a salt
password_provided = 'secret'
password = password_provided.encode()

salt = os.urandom(16)

kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend())

key = base64.urlsafe_b64encode(kdf.derive(password))
print("Key with salt: ")
print(key)

# Get the key from the file
file = open(BASE + '/keys/key.key', 'rb')
key = file.read()
file.close()

#  Open the file to encrypt
with open(BASE + '/in/sensitive.csv', 'rb') as f:
    data = f.read()

fernet = Fernet(key)
encrypted = fernet.encrypt(data)

# Write the encrypted file
with open(BASE + '/out/sensitive.csv.enc', 'wb') as f:
    f.write(encrypted)

print("CHECK THE ENCRYPTED FILE INSIDE out FOLDER")

# You’re taking a weak, human-readable password "secret", mixing in a random salt, and running it through PBKDF2-HMAC with SHA256 many times. The result is a long, random-looking, cryptographically strong 256-bit key, formatted in base64 so it can be used with Fernet for encryption/decryption.