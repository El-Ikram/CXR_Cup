
import base64
import os
import sys

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet


def decrypt_submission(encrypted_file_path):

    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Load private key
    private_key_b64 = os.environ.get("PRIVATE_KEY_B64")

    if not private_key_b64:
        raise ValueError("Private key secret was not found!")

    private_key_pem = base64.b64decode(private_key_b64)

    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None
    )

    # Read encrypted submission
    with open(encrypted_file_path, "rb") as f:
        encrypted_file_data = f.read()

    # Determine RSA encrypted key size
    rsa_size = private_key.key_size // 8

    # Separate encrypted session key and encrypted CSV
    encrypted_session_key = encrypted_file_data[:rsa_size]
    encrypted_data = encrypted_file_data[rsa_size:]

    # Decrypt session key using RSA
    session_key = private_key.decrypt(
        encrypted_session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Decrypt CSV using Fernet
    cipher_suite = Fernet(session_key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)

    # Output CSV filename
    output_file = encrypted_file_path[:-4] + ".csv"

    with open(output_file, "wb") as f:
        f.write(decrypted_data)

    print("Submission decrypted successfully!")
    print("Output file:", output_file)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python decrypt_submission.py <encrypted_file>")
    else:
        decrypt_submission(sys.argv[1])
