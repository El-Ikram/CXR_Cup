
import os
import sys

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet


def encrypt_submission(input_file_path):

    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Load public key
    key_path = os.path.join(script_dir, "public_key.pem")

    with open(key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )

    # Generate session key
    session_key = Fernet.generate_key()
    cipher_suite = Fernet(session_key)

    # Read submission CSV
    with open(input_file_path, "rb") as f:
        file_data = f.read()

    # Encrypt CSV using Fernet
    encrypted_data = cipher_suite.encrypt(file_data)

    # Encrypt session key using RSA
    encrypted_session_key = public_key.encrypt(
        session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Save encrypted submission
    output_file = input_file_path + ".enc"

    with open(output_file, "wb") as f:
        f.write(encrypted_session_key)
        f.write(encrypted_data)

    print("Submission encrypted successfully!")
    print("Output file:", output_file)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python encrypt_submission.py <filename>")
    else:
        encrypt_submission(sys.argv[1])
