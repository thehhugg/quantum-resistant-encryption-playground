#!/usr/bin/env python3
"""
ML-KEM (Kyber) Key Encapsulation Mechanism — Interactive Example
================================================================

This script demonstrates the full lifecycle of the Module-Lattice-Based
Key-Encapsulation Mechanism (ML-KEM), standardized by NIST as FIPS 203.

ML-KEM is the primary post-quantum key encapsulation mechanism selected by
NIST to replace classical key exchanges like Diffie-Hellman and ECDH, which
are vulnerable to Shor's algorithm on a sufficiently large quantum computer.

What this script does
---------------------
1. **Key Generation (keygen):** Produces an *encapsulation key* (public) and a
   *decapsulation key* (private). The encapsulation key can be shared openly;
   the decapsulation key must be kept secret.

2. **Encapsulation (encaps):** Using only the public encapsulation key, a
   sender generates a random *shared secret* and a *ciphertext* that encodes
   it. The shared secret is 32 bytes of high-entropy keying material.

3. **Decapsulation (decaps):** The holder of the private decapsulation key
   recovers the same shared secret from the ciphertext.

The shared secret can then be used as a symmetric key (e.g., for AES-256)
to encrypt actual data. This two-step pattern — asymmetric KEM followed by
symmetric encryption — is how TLS 1.3 and other protocols work.

Parameter sets
--------------
ML-KEM defines three parameter sets that trade off security for performance:

| Parameter Set | Security Level | Encaps Key | Decaps Key | Ciphertext |
|---------------|----------------|------------|------------|------------|
| ML-KEM-512   | NIST Level 1   | 800 B      | 1,632 B    | 768 B      |
| ML-KEM-768   | NIST Level 3   | 1,184 B    | 2,400 B    | 1,088 B    |
| ML-KEM-1024  | NIST Level 5   | 1,568 B    | 3,168 B    | 1,568 B    |

NIST Level 1 is roughly equivalent to AES-128; Level 5 to AES-256.

Dependencies
------------
    pip install kyber-py

Usage
-----
    python examples/01_ml_kem_keygen.py

References
----------
- NIST FIPS 203: https://csrc.nist.gov/pubs/fips/203/final
- kyber-py: https://github.com/GiacomoPope/kyber-py

WARNING: kyber-py is an educational implementation. It is NOT constant-time
and must NOT be used for production cryptography.
"""

import time
import sys

try:
    from kyber_py.ml_kem import ML_KEM_512, ML_KEM_768, ML_KEM_1024
except ImportError:
    print("Error: kyber-py is not installed.")
    print("Install it with:  pip install kyber-py")
    sys.exit(1)


# ─── Configuration ───────────────────────────────────────────────────────────
# Each entry is (human-readable name, ML-KEM class instance).
PARAMETER_SETS = [
    ("ML-KEM-512  (NIST Level 1)", ML_KEM_512),
    ("ML-KEM-768  (NIST Level 3)", ML_KEM_768),
    ("ML-KEM-1024 (NIST Level 5)", ML_KEM_1024),
]


def demonstrate_kem(name: str, kem) -> None:
    """Run the full keygen → encaps → decaps cycle for one parameter set.

    Args:
        name: Human-readable label for this parameter set.
        kem:  An ML-KEM instance (e.g., ML_KEM_512).
    """
    print(f"\n{'=' * 60}")
    print(f"  {name}")
    print(f"{'=' * 60}")

    # ── Step 1: Key Generation ───────────────────────────────────────────
    # The keygen function returns two byte strings:
    #   ek (encapsulation key) — the public key, safe to share
    #   dk (decapsulation key) — the private key, must be kept secret
    t0 = time.perf_counter()
    ek, dk = kem.keygen()
    keygen_ms = (time.perf_counter() - t0) * 1000

    print(f"\n  1. Key Generation ({keygen_ms:.1f} ms)")
    print(f"     Encapsulation key (public):  {len(ek):,} bytes")
    print(f"     Decapsulation key (private): {len(dk):,} bytes")

    # ── Step 2: Encapsulation ────────────────────────────────────────────
    # Anyone with the public encapsulation key can produce:
    #   key — a 32-byte shared secret (random, high-entropy)
    #   ct  — a ciphertext that encodes the shared secret
    t0 = time.perf_counter()
    key, ct = kem.encaps(ek)
    encaps_ms = (time.perf_counter() - t0) * 1000

    print(f"\n  2. Encapsulation ({encaps_ms:.1f} ms)")
    print(f"     Ciphertext size:  {len(ct):,} bytes")
    print(f"     Shared secret:    {key.hex()[:32]}...")

    # ── Step 3: Decapsulation ────────────────────────────────────────────
    # The holder of the private decapsulation key recovers the same
    # shared secret from the ciphertext.
    t0 = time.perf_counter()
    recovered_key = kem.decaps(dk, ct)
    decaps_ms = (time.perf_counter() - t0) * 1000

    print(f"\n  3. Decapsulation ({decaps_ms:.1f} ms)")
    print(f"     Recovered secret: {recovered_key.hex()[:32]}...")

    # ── Verification ─────────────────────────────────────────────────────
    # Both parties now hold the same 32-byte shared secret, which can be
    # used as a symmetric key for AES-256-GCM or similar.
    secrets_match = key == recovered_key
    status = "PASS" if secrets_match else "FAIL"
    print(f"\n  Shared secrets match: {secrets_match}  [{status}]")

    if not secrets_match:
        print("  ERROR: Decapsulation produced a different shared secret!")
        sys.exit(1)


def main() -> None:
    """Run the ML-KEM demonstration for all three parameter sets."""
    print("=" * 60)
    print("  ML-KEM (FIPS 203) Key Encapsulation Demonstration")
    print("=" * 60)
    print()
    print("  This demo shows the keygen → encaps → decaps cycle for")
    print("  all three ML-KEM parameter sets. The shared secret produced")
    print("  by encapsulation and decapsulation should always match.")
    print()
    print("  NOTE: kyber-py is an educational implementation.")
    print("  Do NOT use it for production cryptography.")

    for name, kem in PARAMETER_SETS:
        demonstrate_kem(name, kem)

    print(f"\n{'=' * 60}")
    print("  All parameter sets passed successfully.")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
