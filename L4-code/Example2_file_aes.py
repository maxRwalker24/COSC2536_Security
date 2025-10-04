# THIS IS NOT THE BEST APPROACH
# WE NEED TO LEARN BASICS FIRST AND THEN MORE ADVANCED
# YOU WILL LEARN MORE ELEGANT APPROACH IN LECTORIAL 5

# import required module
from cryptography.fernet import Fernet
import os.path

#for making paths working on all OS
BASE=os.path.dirname(os.path.abspath(__file__))

# key generation
key = Fernet.generate_key()

# string the key in a file
with open(BASE + '/keys/filekey.key', 'wb') as filekey:
    filekey.write(key)

# opening the key
with open(BASE +'/keys/filekey.key', 'rb') as filekey:
	key = filekey.read()

# using the generated key
fernet = Fernet(key)

# opening the original file to encrypt
with open(BASE + '/in/sensitive.csv', 'rb') as file:
	original = file.read()
	
# encrypting the file
encrypted = fernet.encrypt(original)

# opening the file in write mode and 
# writing the encrypted data
with open(BASE + '/out/sensitive_enc', 'wb') as encrypted_file:
	encrypted_file.write(encrypted)

# decryption
# using the key
fernet = Fernet(key)

# opening the encrypted file
with open(BASE + '/out/sensitive_enc', 'rb') as enc_file:
	encrypted = enc_file.read()

# decrypting the file
decrypted = fernet.decrypt(encrypted)

# opening the file in write mode and
# writing the decrypted data
with open(BASE + '/out/sensitive_dec', 'wb') as dec_file:
	dec_file.write(decrypted)
