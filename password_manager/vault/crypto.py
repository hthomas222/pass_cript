# vault/crypto.py
from cryptography.fernet import Fernet
from django.conf import settings


def get_cipher():
    return Fernet(settings.ENCRYPTION_KEY)


def encrypt_password(plain_text: str) -> str:
    """Converts a plain text password into a secure encrypted string."""
    cipher = get_cipher()
    encrypted_bytes = cipher.encrypt(plain_text.encode())
    return encrypted_bytes.decode()


def decrypt_password(cipher_text: str) -> str:
    """Converts the encrypted string back into readable plain text."""
    cipher = get_cipher()
    decrypted_bytes = cipher.decrypt(cipher_text.encode())
    return decrypted_bytes.decode()
