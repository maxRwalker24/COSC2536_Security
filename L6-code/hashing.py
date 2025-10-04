import hashlib
import hmac # for keyed hash

# How to generate a simple hash
text = "Security in Computing & IT"
hash_object = hashlib.sha256(text.encode())
# hexdigest() function is then used to convert the 
# hash object into a hexadecimal string, which is printed out.
print("Simple hash: " + hash_object.hexdigest())


# How to generate a key based hash
def generate_hmac(message, key):
	# Create a new HMAC object
	hmac_object = hmac.new(key.encode(), message.encode(), hashlib.sha256)
	# Return the hexadecimal HMAC value
	return hmac_object.hexdigest()


# Example usage
message = "Security in Computing & IT"
key = "secret_key"
hmac_value = generate_hmac(message, key)
print(f"HMAC: {hmac_value}")
