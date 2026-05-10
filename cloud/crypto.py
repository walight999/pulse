"""End-to-end encryption — Phase 1 stub.

Master key derivation: Argon2id(password, salt=pulse_account_id, m=64MB, t=3, p=1)
Per-row encryption: AES-256-GCM with 12-byte random nonce per row.

Server NEVER sees the master key. Lost password = lost data.
"""
from __future__ import annotations


def derive_master_key(password: str, salt: bytes) -> bytes:
    """Argon2id derivation. Returns 32-byte AES key."""
    raise NotImplementedError("Phase 1 — `argon2-cffi` or `passlib`")


def encrypt_row(plaintext: bytes, master_key: bytes) -> tuple[bytes, bytes]:
    """Returns (ciphertext, nonce). AES-GCM."""
    raise NotImplementedError("Phase 1 — `cryptography.hazmat.primitives.ciphers.aead.AESGCM`")


def decrypt_row(ciphertext: bytes, nonce: bytes, master_key: bytes) -> bytes:
    raise NotImplementedError("Phase 1 — same library, decrypt")


def hash_searchable(value: str, secret_prefix: bytes) -> str:
    """HMAC-SHA-256(secret_prefix || value) — for server-side filtering of
    encrypted rows without revealing plaintext."""
    raise NotImplementedError("Phase 1 — `hmac` + `hashlib.sha256`")
