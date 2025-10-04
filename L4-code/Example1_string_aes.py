from cryptography.fernet import Fernet
key=Fernet.generate_key()
fernet = Fernet(key)
print(key)

#plaintext
msg="Security in Computing & IT".encode()
#ciphertext
encrypted_msg=fernet.encrypt(msg)
decrypted_msg=fernet.decrypt(encrypted_msg)
decrypted_msg=decrypted_msg.decode()

print("Original Message: ", msg.decode())
print("Encrypted Message: ", encrypted_msg)
print("Decrypted Message: ", decrypted_msg)

'''
The decrypted output has a ‘b’ in front of the original message which 
indicates the byte format. However, as you can see 
this can be removed using the decode() method while printing the original message. 
'''