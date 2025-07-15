from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64

# Function to load RSA public key
def load_public_key(public_key_file='public_key.pem'):
    with open(public_key_file, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())
    return public_key

# Function to encrypt AES key using RSA public key
def encrypt_aes_key(aes_key, public_key_file='public_key.pem'):
    public_key = load_public_key(public_key_file)
    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_aes_key

# AES encryption for the file
def aes_encrypt_file(input_file, output_file, aes_key, iv):
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    encryptor = cipher.encryptor()

    with open(input_file, 'rb') as infile:
        file_data = infile.read()
    
    encrypted_data = encryptor.update(file_data) + encryptor.finalize()

    with open(output_file, 'wb') as outfile:
        outfile.write(encrypted_data)

# Main function to perform encryption
def encrypt_file(input_file, output_file, public_key_file='public_key.pem'):
    # Generate random AES key and IV (Initialization Vector)
    aes_key = os.urandom(32)  # AES-256 key
    iv = os.urandom(16)

    # Encrypt AES key with RSA public key
    encrypted_aes_key = encrypt_aes_key(aes_key, public_key_file)

    # Encrypt the file using AES encryption
    aes_encrypt_file(input_file, output_file, aes_key, iv)

    # Return the encrypted AES key and IV for storage/transport
    return base64.b64encode(encrypted_aes_key), base64.b64encode(iv)

if __name__ == "__main__":
    encrypted_key, iv = encrypt_file('example.txt', 'encrypted_example.txt')
    print(f"Encrypted AES key: {encrypted_key.decode()}")
    print(f"IV: {iv.decode()}")
