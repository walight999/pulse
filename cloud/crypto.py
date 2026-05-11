"""End-to-end encryption — production-ready AES-GCM + Argon2id.

Master key derivation: Argon2id(password, salt=pulse_account_id, m=64MB, t=3, p=1)
Per-row encryption: AES-256-GCM with 12-byte random nonce per row.

Server NEVER sees the master key. Lost password = lost data (intentional;
users are warned at signup).

Requires: `cryptography` and `argon2-cffi` (pip install).
"""
from __future__ import annotations

import hashlib
import hmac
import os
import secrets

try:
    from argon2.low_level import hash_secret_raw, Type
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    _CRYPTO_AVAILABLE = True
except ImportError:
    _CRYPTO_AVAILABLE = False


KEY_SIZE = 32          # 256-bit AES key
NONCE_SIZE = 12        # AES-GCM standard
ARGON_TIME_COST = 3
ARGON_MEMORY_KB = 64 * 1024   # 64 MB
ARGON_PARALLELISM = 1


def _require_crypto():
    if not _CRYPTO_AVAILABLE:
        raise RuntimeError(
            "End-to-end encryption requires `cryptography` and `argon2-cffi`. "
            "Install with: pip install cryptography argon2-cffi"
        )


def derive_master_key(password: str, salt: bytes) -> bytes:
    """Argon2id derivation. Returns 32-byte AES key."""
    _require_crypto()
    if len(salt) < 16:
        raise ValueError("salt must be at least 16 bytes")
    return hash_secret_raw(
        secret=password.encode("utf-8"),
        salt=salt,
        time_cost=ARGON_TIME_COST,
        memory_cost=ARGON_MEMORY_KB,
        parallelism=ARGON_PARALLELISM,
        hash_len=KEY_SIZE,
        type=Type.ID,
    )


def encrypt_row(plaintext: bytes, master_key: bytes) -> tuple[bytes, bytes]:
    """Encrypt with AES-256-GCM. Returns (ciphertext_with_tag, nonce)."""
    _require_crypto()
    if len(master_key) != KEY_SIZE:
        raise ValueError(f"master_key must be {KEY_SIZE} bytes")
    nonce = secrets.token_bytes(NONCE_SIZE)
    cipher = AESGCM(master_key)
    ciphertext = cipher.encrypt(nonce, plaintext, associated_data=None)
    return ciphertext, nonce


def decrypt_row(ciphertext: bytes, nonce: bytes, master_key: bytes) -> bytes:
    _require_crypto()
    cipher = AESGCM(master_key)
    return cipher.decrypt(nonce, ciphertext, associated_data=None)


def hash_searchable(value: str, secret_prefix: bytes) -> str:
    """HMAC-SHA-256(secret_prefix || value) — used to build searchable indexes
    on encrypted columns without revealing plaintext to the server."""
    return hmac.new(
        secret_prefix,
        value.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def new_salt() -> bytes:
    """Generate a 32-byte random salt for new accounts."""
    return secrets.token_bytes(32)


def crypto_self_test() -> bool:
    """Round-trip encrypt/decrypt to verify install."""
    try:
        key = derive_master_key("test-password-123", new_salt())
        plaintext = b"hello world"
        ct, nonce = encrypt_row(plaintext, key)
        recovered = decrypt_row(ct, nonce, key)
        return recovered == plaintext
    except Exception:
        return False
