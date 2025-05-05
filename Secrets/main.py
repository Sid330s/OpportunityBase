import hashlib
from cryptography.fernet import Fernet
import base64
import hashlib


def password_to_key(password: str) -> bytes:
    """Converts password to a 32-byte Fernet key using SHA-256."""
    sha = hashlib.sha256()
    sha.update(password.encode())
    return base64.urlsafe_b64encode(sha.digest())


def encrypt_file(input_file: str, output_file: str, password: str):
    key = password_to_key(password)
    fernet = Fernet(key)

    with open(input_file, 'rb') as f:
        data = f.read()

    encrypted_data = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted_data)


def decrypt_file(encrypted_file: str, output_file: str, password: str):
    key = password_to_key(password)
    fernet = Fernet(key)

    with open(encrypted_file, 'rb') as f:
        encrypted_data = f.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    with open(output_file, 'wb') as f:
        f.write(decrypted_data)


if __name__ == "__main__":

    mode = input("Encrypt or Decrypt? (e/d): ").strip().lower()
    password = input("Enter password: ").strip()

    if mode == "e":
        encrypt_file("example.txt", "example_encrypted.bin", password)
        print("File encrypted.")
    elif mode == "d":
        decrypt_file("example_encrypted.bin", "example_decrypted.txt", password)
        print("File decrypted.")
    else:
        print("Invalid option.")
