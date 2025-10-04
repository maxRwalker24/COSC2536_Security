import hashlib as hasher
import datetime as date

# Define what a SnakeCoin block is
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(
            str(self.index).encode("utf-8") +
            str(self.timestamp).encode("utf-8") +
            str(self.data).encode("utf-8") +
            str(self.previous_hash).encode("utf-8")
        )
        return sha.hexdigest()


# Generate genesis block
def create_genesis_block():
    return Block(0, date.datetime.now(), "Genesis Block", "0")


# Generate all later blocks in the blockchain
def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = f"Hey! I'm block {this_index}"
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)

# NEW ADDITION
# Validate the blockchain
def is_chain_valid(chain):
    for i in range(1, len(chain)):
        current = chain[i]
        previous = chain[i - 1]

        # Recalculate the hash of the current block
        if current.hash != current.hash_block():
            print(f"Block {current.index} has been tampered with!")
            return False

        # Check that the current block points to the correct previous block
        if current.previous_hash != previous.hash:
            print(f"Block {current.index} has wrong previous hash!")
            return False

    return True


# Create the blockchain and add the genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# How many blocks should we add to the chain after the genesis block?
num_of_blocks_to_add = 5

# Add blocks to the chain
for i in range(num_of_blocks_to_add):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    print(f"Block #{block_to_add.index} has been added to the blockchain!")
    print(f"Hash: {block_to_add.hash}\n")

# Validate blockchain
print("Blockchain valid?", is_chain_valid(blockchain))
