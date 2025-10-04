import hashlib

data = "hello world".encode()   # encode string to bytes
# hash_value = hashlib.sha256(data).hexdigest()
hash_value = hashlib.md5(data).hexdigest()

# print("SHA-256:", hash_value)
print("MD5:", hash_value)
