#!/usr/bin/env python3
"""
ML-DSA (Dilithium) Digital Signature — Interactive Example
==========================================================

This script demonstrates the Module-Lattice-Based Digital Signature
Algorithm (ML-DSA), standardized by NIST as FIPS 204.

ML-DSA is the primary post-quantum digital signature scheme selected by
NIST to replace classical signatures like RSA, ECDSA, and EdDSA, which
are vulnerable to Shor's algorithm on a quantum computer.

Key encapsulation vs. digital signatures
----------------------------------------
Post-quantum cryptography has two main pillars:

- **Key Encapsulation (ML-KEM / Kyber):** Lets two parties establish a
  shared secret over an insecure channel. Used for encryption.
  See ``examples/01_ml_kem_keygen.py``.

- **Digital Signatures (ML-DSA / Dilithium):** Lets a signer prove that
  a message is authentic and has not been tampered with. Used for
  authentication, code signing, certificates, and blockchain.

What this script does
---------------------
1. **Key Generation (keygen):** Produces a *public key* (for verification)
   and a *secret key* (for signing).

2. **Signing (sign):** The holder of the secret key produces a *signature*
   over a message. The signature is a byte string that anyone can verify.

3. **Verification (verify):** Anyone with the public key can check that
   the signature is valid for the given message. If the message or
   signature is altered, verification fails.

Parameter sets
--------------
ML-DSA defines three parameter sets:

| Parameter Set | Security Level | Public Key | Secret Key | Signature |
|---------------|----------------|------------|------------|-----------|
| ML-DSA-44     | NIST Level 2   | 1,312 B    | 2,560 B    | 2,420 B   |
| ML-DSA-65     | NIST Level 3   | 1,952 B    | 4,032 B    | 3,309 B   |
| ML-DSA-87     | NIST Level 5   | 2,592 B    | 4,896 B    | 4,627 B   |

For comparison, an ECDSA P-256 signature is only 64 bytes and a public
key is 64 bytes — but those are broken by a quantum computer running
Shor's algorithm.

Dependencies
------------
    pip install dilithium-py

Usage
-----
    python examples/02_ml_dsa_signatures.py

References
----------
- NIST FIPS 204: https://csrc.nist.gov/pubs/fips/204/final
- dilithium-py: https://github.com/GiacomoPope/dilithium-py

WARNING: dilithium-py is an educational implementation. It is NOT
constant-time and must NOT be used for production cryptography.
"""

import time
import sys

try:
    from dilithium_py.ml_dsa import ML_DSA_44, ML_DSA_65, ML_DSA_87
except ImportError:
    print("Error: dilithium-py is not installed.")
    print("Install it with:  pip install dilithium-py")
    sys.exit(1)


# ─── Configuration ───────────────────────────────────────────────────────────
PARAMETER_SETS = [
    ("ML-DSA-44 (NIST Level 2)", ML_DSA_44),
    ("ML-DSA-65 (NIST Level 3)", ML_DSA_65),
    ("ML-DSA-87 (NIST Level 5)", ML_DSA_87),
]

# The message to sign. In practice this could be a document, a software
# binary hash, a TLS handshake transcript, or any byte string.
MESSAGE = b"Post-quantum cryptography protects against future quantum computers."


def demonstrate_signatures(name: str, dsa, message: bytes) -> None:
    """Run the full keygen -> sign -> verify cycle for one parameter set.

    Args:
        name:    Human-readable label for this parameter set.
        dsa:     An ML-DSA instance (e.g., ML_DSA_44).
        message: The message bytes to sign.
    """
    print(f"\n{'=' * 60}")
    print(f"  {name}")
    print(f"{'=' * 60}")

    # ── Step 1: Key Generation ───────────────────────────────────────────
    # keygen() returns:
    #   pk — the public (verification) key, safe to distribute
    #   sk — the secret (signing) key, must be kept private
    t0 = time.perf_counter()
    pk, sk = dsa.keygen()
    keygen_ms = (time.perf_counter() - t0) * 1000

    print(f"\n  1. Key Generation ({keygen_ms:.1f} ms)")
    print(f"     Public key (verification):  {len(pk):,} bytes")
    print(f"     Secret key (signing):       {len(sk):,} bytes")

    # ── Step 2: Signing ──────────────────────────────────────────────────
    # sign() takes the secret key and a message, and produces a signature.
    # The signature is deterministic for a given (sk, message) pair in
    # ML-DSA (unlike ECDSA which requires a random nonce).
    t0 = time.perf_counter()
    signature = dsa.sign(sk, message)
    sign_ms = (time.perf_counter() - t0) * 1000

    print(f"\n  2. Signing ({sign_ms:.1f} ms)")
    print(f"     Message:        \"{message.decode()}\"")
    print(f"     Signature size: {len(signature):,} bytes")
    print(f"     Signature hex:  {signature.hex()[:32]}...")

    # ── Step 3: Verification ─────────────────────────────────────────────
    # verify() takes the public key, the original message, and the
    # signature. It returns True if the signature is valid.
    t0 = time.perf_counter()
    is_valid = dsa.verify(pk, message, signature)
    verify_ms = (time.perf_counter() - t0) * 1000

    status = "PASS" if is_valid else "FAIL"
    print(f"\n  3. Verification ({verify_ms:.1f} ms)")
    print(f"     Signature valid: {is_valid}  [{status}]")

    if not is_valid:
        print("  ERROR: Signature verification failed!")
        sys.exit(1)

    # ── Step 4: Tamper Detection ─────────────────────────────────────────
    # If we modify even one byte of the message, verification must fail.
    # This is the whole point of a digital signature.
    tampered_message = message + b"!"
    tamper_valid = dsa.verify(pk, tampered_message, signature)
    tamper_status = "PASS (correctly rejected)" if not tamper_valid else "FAIL"
    print(f"\n  4. Tamper Detection")
    print(f"     Modified message verified: {tamper_valid}  [{tamper_status}]")

    if tamper_valid:
        print("  ERROR: Tampered message was incorrectly accepted!")
        sys.exit(1)


def main() -> None:
    """Run the ML-DSA demonstration for all three parameter sets."""
    print("=" * 60)
    print("  ML-DSA (FIPS 204) Digital Signature Demonstration")
    print("=" * 60)
    print()
    print("  This demo shows the keygen -> sign -> verify cycle for")
    print("  all three ML-DSA parameter sets, plus tamper detection.")
    print()
    print("  NOTE: dilithium-py is an educational implementation.")
    print("  Do NOT use it for production cryptography.")

    for name, dsa in PARAMETER_SETS:
        demonstrate_signatures(name, dsa, MESSAGE)

    print(f"\n{'=' * 60}")
    print("  All parameter sets passed successfully.")
    print("  All tamper detection checks passed.")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
