import hashlib

# Example block data
block_data = "This is some block data"

# Target difficulty (number of leading zeros required)
difficulty = 7
target = "0" * difficulty

nonce = 0
found = False

print("Starting proof-of-work...")

while not found:
    # Combine block data and nonce
    text = block_data + str(nonce)
    
    # Compute SHA-256 hash
    hash_result = hashlib.sha256(text.encode()).hexdigest()
    
    # Check if hash meets the target difficulty
    if hash_result.startswith(target):
        found = True
        print(f"Nonce found: {nonce}")
        print(f"Hash: {hash_result}")
    else:
        nonce += 1
