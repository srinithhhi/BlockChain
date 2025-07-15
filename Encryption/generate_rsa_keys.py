from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_keys(private_key_file='private_key.pem', public_key_file='public_key.pem'):
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Write private key to file
    with open(private_key_file, 'wb') as private_file:
        private_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )
    
    # Generate public key
    public_key = private_key.public_key()
    
    # Write public key to file
    with open(public_key_file, 'wb') as public_file:
        public_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )
    
    print(f"Keys generated. Private key saved to {private_key_file}, public key saved to {public_key_file}.")

if __name__ == "__main__":
    generate_rsa_keys()
