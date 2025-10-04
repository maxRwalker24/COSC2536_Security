"""
task3-hide-and-seek.py
Assignment 2, Question 4: Steganography with AES (Metadata Approach)

This program demonstrates metadata-based steganography in JPEG images. 
It encrypts a user-provided plaintext message using AES (CBC mode with PKCS7 padding), then embeds the ciphertext into the JPEG file's comment metadata segment. It can extract and decrypt the hidden message.

References:
1. AES encryption and CBC mode: Cryptography library documentation
   https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/
2. Metadata steganography (JPEG comments): 
   https://en.wikipedia.org/wiki/Steganography#In_images
3. JPEG COM segment structure:
   https://en.wikipedia.org/wiki/JPEG_File_Interchange_Format 
4. JPEG Metadata details: 
   https://dev.exiv2.org/projects/exiv2/wiki/The_Metadata_in_JPEG_files
5. COSC2536 Practical 7 "aes_cbc_file.py" AES encryption/decryption sample code 
6. Python binascii module documentation: 
   https://docs.python.org/3/library/binascii.html

"""

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
import webbrowser
import binascii

# BASE variable for cross-platform paths
BASE = os.path.dirname(os.path.abspath(__file__))

# AES Encryption / Decryption adapted from COSC2536 Practical 7 "aes_cbc_file.py"
def encrypt_message(message: str, password: str) -> bytes:
    """
    Encrypts a plaintext string using AES-256-CBC with PKCS7 padding.
    Returns the concatenation: salt + IV + ciphertext.

    Rationale:
    - PBKDF2 with SHA256 strengthens the password into a 256-bit key.
    - Random salt ensures that the same password produces different keys each run.
    - Random IV ensures that repeated messages encrypt differently.
    - PKCS7 padding ensures plaintext length is multiple of AES block size (16 bytes).
    """
    salt = os.urandom(16)  # 16-byte random salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password.encode())

    iv = os.urandom(16)  # 16-byte IV for CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    plaintext_bytes = message.encode('utf-8')
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext_bytes) + padder.finalize()

    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return salt + iv + ciphertext  # store salt+IV for decryption


def decrypt_message(encrypted_data: bytes, password: str) -> str:
    """
    Decrypts data previously encrypted with encrypt_message.
    Expects encrypted_data = salt + IV + ciphertext
    """
    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password.encode())

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext_bytes = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext_bytes.decode('utf-8')


"""
Metadata Steganography (JPEG COM segment)
JPEG File Structure with Embedded Encrypted Message (COM Segment)

Example:

SOI:        FF D8
COM marker: FF FE
Length:     00 1A  (26 bytes total including these 2 bytes)
Hex data:   5f2a8c...  (hex representation of AES-encrypted message)
JPEG Data:  FF DB ... (remaining normal JPEG segments)

Explanation:

1. SOI marker (FFD8): Indicates start of JPEG file.
2. COM marker (FFFE): Signifies a comment segment.
3. Length field (2 bytes): Specifies total length of COM segment, including these 2 bytes.
4. Hex-encoded encrypted message: The actual secret message is AES-encrypted and converted to hex for safe storage.
5. JPEG Image Data: Original image content remains unchanged, so the image looks identical to the human eye.

Notes:
- Hex encoding ensures all bytes are valid and avoids conflicts with JPEG markers.
- Extracting the message involves locating the COM segment, reading the length, and decoding the hex back to the original encrypted bytes.
- LSB steganography is avoided because JPEG compression can corrupt pixel-level changes.
"""


def embed_message_in_jpeg(cover_jpeg_path: str, stego_jpeg_path: str, encrypted_message: bytes):
    """
    Embed encrypted message into JPEG comment segment.

    Rationale:
    - LSB steganography is not reliable for JPEG due to compression.
    - COM segment (0xFFFE) can safely store extra data without affecting visible image.
    - Hex encoding of encrypted bytes ensures printable metadata characters and avoids byte conflicts.
    - COM segment structure:
        0xFF 0xFE        : COM marker
        2-byte length     : total length including these 2 bytes
        data              : hex-encoded encrypted message
    """
    # Opens the image in binary mode. Converts the file to a bytearray so I can insert new bytes (COM segment).
    with open(cover_jpeg_path, 'rb') as f:
        jpeg_bytes = bytearray(f.read())

    # JPEG files always start with the SOI (Start of Image) marker 0xFFD8. If not present, the file is invalid.
    if jpeg_bytes[0:2] != b'\xff\xd8':
        raise ValueError("Not a valid JPEG file")
    
    """
    Below, binascii.hexlify() converts any bytes into a safe ASCII string: Only uses characters 0-9 and a-f. Guaranteed to be safe for embedding in text-based metadata. Reversible with binascii.unhexlify().

    The problem was that AES encryption produces raw bytes that can contain any value from 0x00 to 0xFF. JPEG metadata, especially COM segments expects textual/printable data. Certain byte values (like 0xFF or 0x00) can conflict with JPEG markers, potentially corrupting the file if stored directly. .decode('utf-8') will fail if the bytes are not valid UTF-8.
    """
    hex_message = binascii.hexlify(encrypted_message)  # bytes -> hex string for safe storage
 
    # Construct COM segment
    """
    0xFF 0xFE       - COM marker
    2-byte length   - includes length bytes
    data            - the hex-encoded encrypted message
    """
    com_length = len(hex_message) + 2  # com_length is total length, including the 2 bytes used for the length itself.
    com_bytes = bytearray([0xFF, 0xFE, (com_length >> 8) & 0xFF, com_length & 0xFF]) #com_bytes constructs the COM segment as a byte array.
    com_bytes += hex_message

    # Place the COM segment right after the SOI marker (0xFFD8). This is safe and ensures that JPEG viewers still display the image normally.
    jpeg_bytes = jpeg_bytes[:2] + com_bytes + jpeg_bytes[2:]
    
    # Write the modified byte array to a new file.
    with open(stego_jpeg_path, 'wb') as f:
        f.write(jpeg_bytes)

    # Confirm the file has been saved. Opens it in the default web browser so the user can view it immediately. Note that the image will look identical to the original.
    print(f"Encrypted message embedded in '{stego_jpeg_path}'")
    webbrowser.open(stego_jpeg_path)





def extract_message_from_jpeg(stego_jpeg_path: str) -> bytes:
    """
    Extract the hidden encrypted message from the COM (comment) segment of a JPEG file.

    Rationale:
   
    - JPEG files support a "comment segment" (marker: 0xFFFE) that can store arbitrary data.
    - In my steganography approach, the encrypted message was first hex-encoded and then stored in this COM segment.
    - Hex encoding is used instead of raw ciphertext bytes because:
         Encrypted data may contain invalid characters (non-UTF-8, control bytes).
         Hex encoding ensures the message is stored safely using only ASCII characters (0-9, a-f).
    - This function reverses the embedding procedure:
        Locate the COM marker (0xFFFE).
        Read its 2-byte length field (big-endian).
        Extract the hex string that represents the encrypted message.
        Decode (unhexlify) this string back to the original encrypted bytes.
    """

    # Read the JPEG file fully as binary data
    with open(stego_jpeg_path, 'rb') as f:
        jpeg_bytes = f.read()

    # Search for the COM marker (0xFFFE).
    # The COM marker always begins with 0xFF followed by 0xFE.
    # .find() returns -1 if not found.
    idx = jpeg_bytes.find(b'\xFF\xFE')
    if idx == -1:
        raise ValueError("No COM segment found in JPEG. This image may not contain hidden data.")

    """
    The JPEG specification (Wikipedia JPEG Syntax and structure) defines that after any marker that carries data (like COM, APPn, etc.), two bytes follow which encode the segment length in big-endian. Importantly, this length includes the two length-field bytes but does not include the marker bytes.
    We therefore read:
      high_byte = jpeg_bytes[idx+2]
      low_byte  = jpeg_bytes[idx+3]
      length = high_byte << 8 + low_byte
    Then payload data begins at idx+4, and continues for (length – 2) bytes.

    - jpeg_bytes[idx+2] << 8 shifts the high-order byte left by 8 bits (i.e. multiplies by 256). 
    - Then I add the low-order byte (jpeg_bytes[idx+3]).
    - The result is the integer length of that segment.
    """
    length = (jpeg_bytes[idx+2] << 8) + jpeg_bytes[idx+3]

    """
    -idx + 4 is where the actual data begins (skipping the marker 2 bytes + length 2 bytes).

    - idx + 2 + length is the end of that segment — because length counts from idx+2 through the data.
    """
    hex_message = jpeg_bytes[idx+4 : idx+2+length]

    """
    - Convert hex-encoded string back to original ciphertext bytes.
    - The hex string was created earlier with binascii.hexlify()
    - unhexlify() reverses this process, recovering the exact encrypted bytes
    """
    encrypted_message = binascii.unhexlify(hex_message)

    # Return the raw encrypted bytes.
    #   - These bytes can now be decrypted with AES using the correct key.
    return encrypted_message


# Main workflow
if __name__ == "__main__":
    print("Task 3: Hide and Seek - AES + JPEG Metadata Steganography")
    cover_image = os.path.join(BASE, 'input', 'cover.jpg')
    stego_image = os.path.join(BASE, 'output', 'stego_cover.jpg')

    # Prompt user for a plaintext message
    plaintext_message = input("Enter the message to hide: ")

    # Prompt user for a password for AES encryption
    password = input("Enter a password to encrypt the message: ")

    # Encrypt the message
    encrypted_msg = encrypt_message(plaintext_message, password)

    # Display the encrypted message
    # Note: encrypted bytes may contain non-printable characters.
    # To display safely I hex-encode them.
    print("\nEncrypted message (hex-encoded for display):")
    print(binascii.hexlify(encrypted_msg).decode('utf-8'))

    # Embed encrypted message into JPEG metadata
    embed_message_in_jpeg(cover_image, stego_image, encrypted_msg)

    # Extract and decrypt to verify
    extracted_encrypted = extract_message_from_jpeg(stego_image)

    # Optional: Show the raw extracted hex to prove correctness
    print("\nExtracted encrypted message (hex-encoded):")
    print(binascii.hexlify(extracted_encrypted).decode('utf-8'))

    # Prompt user for same password for AES encryption
    password_2 = input("Re-enter your password to decrypt the message: ")

    while password != password_2:
        print("Warning: Passwords do not match! ")
        password_2 = input("Re-enter your password to decrypt the message: ")

    # Decrypt the extracted message
    decrypted_message = decrypt_message(extracted_encrypted, password_2)

    print("\nPassword accepted. Decrypted message retrieved from stego image:")
    print(decrypted_message)
    print("__" * 40)



