from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

# Function to load RSA private key
def load_private_key(private_key_file='private_key.pem'):
    with open(private_key_file, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )
    return private_key

# Function to decrypt AES key using RSA private key
def decrypt_aes_key(encrypted_aes_key, private_key_file='private_key.pem'):
    private_key = load_private_key(private_key_file)
    decrypted_aes_key = private_key.decrypt(
        base64.b64decode(encrypted_aes_key),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_aes_key

# AES decryption for the file
def aes_decrypt_file(input_file, output_file, aes_key, iv):
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(base64.b64decode(iv)))
    decryptor = cipher.decryptor()

    with open(input_file, 'rb') as infile:
        encrypted_data = infile.read()

    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    with open(output_file, 'wb') as outfile:
        outfile.write(decrypted_data)

# Main function to perform decryption
def decrypt_file(input_file, output_file, encrypted_key, iv, private_key_file='private_key.pem'):
    aes_key = decrypt_aes_key(encrypted_key, private_key_file)
    aes_decrypt_file(input_file, output_file, aes_key, iv)

if __name__ == "__main__":
    # Example usage
    encrypted_key = "Base64_encoded_encrypted_key"
    iv = "Base64_encoded_iv"
    decrypt_file('encrypted_example.txt', 'decrypted_example.txt', encrypted_key, iv)
