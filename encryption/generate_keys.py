
import os
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


if __name__ == "__main__":

    # Define key locations
    BASE_DIR = Path(__file__).resolve().parent

    private_path = BASE_DIR / "private_key.pem"
    public_path = BASE_DIR.parent / "participant_files" / "public_key.pem"

    # Prevent overwriting existing keys
    if private_path.exists() or public_path.exists():
        print("Warning: Key files already exist.")
        print("Generating new keys may prevent decryption of previous submissions.")
        raise SystemExit(1)

    # Generate RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Serialize private key without password protection
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Generate public key
    public_key = private_key.public_key()

    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Create public key directory
    public_path.parent.mkdir(parents=True, exist_ok=True)

    # Save private key
    with open(private_path, "xb") as f:
        f.write(pem_private)

    # Save public key
    with open(public_path, "xb") as f:
        f.write(pem_public)

    print("Keys generated successfully!")
    print("Private key:", private_path)
    print("Public key:", public_path)
