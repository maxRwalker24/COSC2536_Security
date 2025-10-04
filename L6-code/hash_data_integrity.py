import hashlib
import os

# to make path work on all OS
BASE = os.path.dirname(os.path.abspath(__file__))

# calculate hash of a file
def calculate_sha256(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

# check the data integrity
def check_integrity(original_file_path, transmitted_file_path):
    """Check the integrity of two files by comparing their SHA-256 hashes."""
    original_hash = calculate_sha256(original_file_path)
    transmitted_hash = calculate_sha256(transmitted_file_path)

    print(f"Original file hash:    {original_hash}")
    print(f"Transmitted file hash: {transmitted_hash}")

    if original_hash == transmitted_hash:
        print("Integrity Check: PASSED (Files are identical)")
    else:
        print("Integrity Check: FAILED (Files differ)")

def main():
    # Define the file paths relative to the BASE directory
    original_file = os.path.join(BASE, 'assets', 'file.txt')
    transmitted_file = os.path.join(BASE, 'assets', 'transmitted.txt')

    # Perform the integrity check
    check_integrity(original_file, transmitted_file)

if __name__ == "__main__":
    main()
