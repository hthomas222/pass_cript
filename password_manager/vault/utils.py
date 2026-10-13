# vault/utils.py
import base64
import hashlib
from cryptography.fernet import Fernet
from django.conf import settings


def get_fernet_key() -> bytes:
    """Derives a deterministic, 32-byte URL-safe Fernet key from Django's SECRET_KEY."""
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return base64.urlsafe_b64encode(key)


def encrypt_password(raw_password: str) -> str:
    """Encrypts a plaintext string into Fernet ciphertext."""
    f = Fernet(get_fernet_key())
    return f.encrypt(raw_password.encode()).decode()


def decrypt_password(encrypted_password: str) -> str:
    """Decrypts Fernet ciphertext back into plaintext."""
    f = Fernet(get_fernet_key())
    return f.decrypt(encrypted_password.encode()).decode()