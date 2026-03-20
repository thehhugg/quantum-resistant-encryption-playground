#!/usr/bin/env python3
"""
BB84 Quantum Key Distribution — Educational Simulation
=======================================================

This module simulates the BB84 protocol, the first quantum key
distribution (QKD) scheme, proposed by Bennett and Brassard in 1984.

What BB84 does
--------------
BB84 allows two parties (Alice and Bob) to establish a shared secret
key over a public channel, with the guarantee that any eavesdropper
(Eve) will be detected. The security comes from the laws of quantum
mechanics, not from computational hardness assumptions.

How it works
------------
1. **Alice prepares qubits.** For each bit of the key, Alice randomly
   chooses a basis (rectilinear + or diagonal x) and a bit value (0 or 1).
   She encodes the bit in the chosen basis and sends the qubit to Bob.

2. **Bob measures.** Bob randomly chooses a basis for each qubit and
   measures it. If he chose the same basis as Alice, he gets the correct
   bit. If not, he gets a random result.

3. **Basis reconciliation.** Alice and Bob publicly announce their basis
   choices (but NOT the bit values). They keep only the bits where they
   used the same basis. This is the "sifted key."

4. **Eavesdropper detection.** They sacrifice a random subset of the
   sifted key to check for errors. If Eve intercepted and re-sent
   qubits, she would have introduced errors (~25% error rate). If the
   error rate is below a threshold, the remaining bits form the key.

BB84 vs. Post-Quantum Cryptography
-----------------------------------
BB84 and PQC solve different problems:
- **BB84 (QKD):** Requires a quantum channel (fiber optic or free-space).
  Provides information-theoretic security. Limited range (~100 km).
- **PQC (ML-KEM, ML-DSA):** Runs on classical hardware and networks.
  Provides computational security against quantum computers.

Both are part of the quantum-safe toolkit, but PQC is far more practical
for most applications today.

Dependencies
------------
    pip install numpy

Usage
-----
    python quantum/bb84_simulation.py
    python quantum/bb84_simulation.py --bits 256
    python quantum/bb84_simulation.py --bits 128 --eavesdrop
"""

import argparse
import sys

import numpy as np


# ─── BB84 Protocol ──────────────────────────────────────────────────────────

# Basis constants
RECTILINEAR = 0  # + basis: |0>, |1>
DIAGONAL = 1     # x basis: |+>, |->


def alice_prepare(n_bits: int) -> tuple:
    """Alice prepares n qubits with random bases and bit values.

    Returns:
        alice_bits:  Array of random bit values (0 or 1).
        alice_bases: Array of random basis choices (0=rectilinear, 1=diagonal).
    """
    alice_bits = np.random.randint(0, 2, size=n_bits)
    alice_bases = np.random.randint(0, 2, size=n_bits)
    return alice_bits, alice_bases


def bob_measure(alice_bits: np.ndarray, alice_bases: np.ndarray) -> tuple:
    """Bob measures each qubit in a randomly chosen basis.

    If Bob's basis matches Alice's, he gets the correct bit.
    If not, he gets a random result (50/50).

    Returns:
        bob_bits:  Array of Bob's measurement results.
        bob_bases: Array of Bob's basis choices.
    """
    n_bits = len(alice_bits)
    bob_bases = np.random.randint(0, 2, size=n_bits)
    bob_bits = np.zeros(n_bits, dtype=int)

    for i in range(n_bits):
        if bob_bases[i] == alice_bases[i]:
            # Same basis: Bob gets the correct bit
            bob_bits[i] = alice_bits[i]
        else:
            # Different basis: random result
            bob_bits[i] = np.random.randint(0, 2)

    return bob_bits, bob_bases


def eve_intercept(alice_bits: np.ndarray, alice_bases: np.ndarray) -> np.ndarray:
    """Eve intercepts, measures in a random basis, and re-sends.

    Eve doesn't know Alice's bases, so she guesses randomly.
    When she guesses wrong, she disturbs the qubit state.

    Returns:
        intercepted_bits: The bits as modified by Eve's measurement.
    """
    n_bits = len(alice_bits)
    eve_bases = np.random.randint(0, 2, size=n_bits)
    intercepted_bits = np.copy(alice_bits)

    for i in range(n_bits):
        if eve_bases[i] != alice_bases[i]:
            # Eve measured in the wrong basis: the qubit is now random
            intercepted_bits[i] = np.random.randint(0, 2)

    return intercepted_bits


def sift_key(alice_bits: np.ndarray, alice_bases: np.ndarray,
             bob_bits: np.ndarray, bob_bases: np.ndarray) -> tuple:
    """Keep only the bits where Alice and Bob used the same basis.

    Returns:
        alice_sifted: Alice's bits at matching positions.
        bob_sifted:   Bob's bits at matching positions.
    """
    matching = alice_bases == bob_bases
    return alice_bits[matching], bob_bits[matching]


def check_for_eavesdropper(alice_sifted: np.ndarray, bob_sifted: np.ndarray,
                           sample_fraction: float = 0.5) -> tuple:
    """Sacrifice a fraction of the sifted key to detect eavesdropping.

    Alice and Bob publicly compare a random subset of their sifted bits.
    If the error rate exceeds the threshold, an eavesdropper is present.

    Returns:
        error_rate:    Fraction of mismatched bits in the sample.
        final_key_alice: Alice's remaining key bits (after removing the sample).
        final_key_bob:   Bob's remaining key bits.
    """
    n = len(alice_sifted)
    sample_size = max(1, int(n * sample_fraction))

    # Random sample indices
    indices = np.random.permutation(n)
    sample_idx = indices[:sample_size]
    key_idx = indices[sample_size:]

    # Check error rate in the sample
    errors = np.sum(alice_sifted[sample_idx] != bob_sifted[sample_idx])
    error_rate = errors / sample_size if sample_size > 0 else 0.0

    # The remaining bits form the final key
    final_key_alice = alice_sifted[key_idx]
    final_key_bob = bob_sifted[key_idx]

    return error_rate, final_key_alice, final_key_bob


# ─── Simulation Runner ──────────────────────────────────────────────────────

def run_bb84(n_bits: int = 128, eavesdrop: bool = False,
             verbose: bool = True) -> dict:
    """Run a full BB84 simulation.

    Args:
        n_bits:    Number of qubits Alice sends.
        eavesdrop: If True, Eve intercepts the qubits.
        verbose:   If True, print step-by-step output.

    Returns:
        A dict with simulation results.
    """
    if verbose:
        print(f"\n  Qubits sent:    {n_bits}")
        print(f"  Eavesdropper:   {'YES (Eve is listening)' if eavesdrop else 'No'}")

    # Step 1: Alice prepares
    alice_bits, alice_bases = alice_prepare(n_bits)
    if verbose:
        print(f"\n  Step 1: Alice prepares {n_bits} qubits")
        if n_bits <= 20:
            print(f"    Bits:  {_bits_str(alice_bits)}")
            print(f"    Bases: {_bases_str(alice_bases)}")

    # Step 2 (optional): Eve intercepts
    transmitted_bits = alice_bits
    if eavesdrop:
        transmitted_bits = eve_intercept(alice_bits, alice_bases)
        if verbose:
            print(f"\n  Step 2: Eve intercepts and re-sends")
            if n_bits <= 20:
                changed = np.sum(transmitted_bits != alice_bits)
                print(f"    Eve disturbed {changed}/{n_bits} qubits")

    # Step 3: Bob measures
    bob_bits, bob_bases = bob_measure(transmitted_bits, alice_bases)
    if verbose:
        print(f"\n  Step 3: Bob measures in random bases")
        if n_bits <= 20:
            print(f"    Bases: {_bases_str(bob_bases)}")
            print(f"    Bits:  {_bits_str(bob_bits)}")

    # Step 4: Basis reconciliation
    alice_sifted, bob_sifted = sift_key(alice_bits, alice_bases,
                                        bob_bits, bob_bases)
    if verbose:
        matching = np.sum(alice_bases == bob_bases)
        print(f"\n  Step 4: Basis reconciliation")
        print(f"    Matching bases: {matching}/{n_bits} ({100*matching/n_bits:.0f}%)")
        print(f"    Sifted key length: {len(alice_sifted)} bits")

    # Step 5: Eavesdropper detection
    error_rate, final_alice, final_bob = check_for_eavesdropper(
        alice_sifted, bob_sifted
    )

    keys_match = np.array_equal(final_alice, final_bob)
    eve_detected = error_rate > 0.11  # Theoretical threshold ~25% with Eve

    if verbose:
        print(f"\n  Step 5: Eavesdropper detection")
        print(f"    Error rate in sample: {error_rate:.1%}")
        print(f"    Expected with Eve:    ~25%")
        print(f"    Expected without Eve: 0%")
        print(f"    Verdict: {'EAVESDROPPER DETECTED' if eve_detected else 'Channel appears secure'}")
        print(f"\n  Final shared key length: {len(final_alice)} bits")
        print(f"  Keys match: {keys_match}")
        if len(final_alice) <= 32 and len(final_alice) > 0:
            print(f"  Alice's key: {_bits_str(final_alice)}")
            print(f"  Bob's key:   {_bits_str(final_bob)}")

    return {
        "n_bits": n_bits,
        "eavesdrop": eavesdrop,
        "sifted_length": len(alice_sifted),
        "final_key_length": len(final_alice),
        "error_rate": error_rate,
        "eve_detected": eve_detected,
        "keys_match": keys_match,
    }


def _bits_str(bits: np.ndarray) -> str:
    """Format a bit array as a string."""
    return "".join(str(b) for b in bits)


def _bases_str(bases: np.ndarray) -> str:
    """Format a basis array as a string (+ for rectilinear, x for diagonal)."""
    return "".join("+" if b == 0 else "x" for b in bases)


# ─── CLI Entry Point ────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulate the BB84 quantum key distribution protocol."
    )
    parser.add_argument(
        "--bits", "-b", type=int, default=128,
        help="Number of qubits to send. Default: 128",
    )
    parser.add_argument(
        "--eavesdrop", "-e", action="store_true",
        help="Simulate an eavesdropper (Eve) on the channel.",
    )
    args = parser.parse_args()

    if args.bits < 10:
        print("Error: need at least 10 bits for a meaningful simulation.")
        sys.exit(1)

    print("=" * 60)
    print("  BB84 Quantum Key Distribution Simulation")
    print("=" * 60)

    # Run without eavesdropper
    print("\n" + "-" * 60)
    print("  Scenario 1: Secure channel (no eavesdropper)")
    print("-" * 60)
    result_clean = run_bb84(args.bits, eavesdrop=False)

    # Run with eavesdropper
    print("\n" + "-" * 60)
    print("  Scenario 2: Eve is eavesdropping")
    print("-" * 60)
    result_eve = run_bb84(args.bits, eavesdrop=True)

    # Summary
    print(f"\n{'=' * 60}")
    print("  Summary")
    print(f"{'=' * 60}")
    print(f"  {'Metric':<30} {'No Eve':>12} {'With Eve':>12}")
    print(f"  {'-'*30} {'-'*12} {'-'*12}")
    print(f"  {'Error rate':<30} {result_clean['error_rate']:>11.1%} {result_eve['error_rate']:>11.1%}")
    print(f"  {'Eve detected':<30} {'No':>12} {'Yes' if result_eve['eve_detected'] else 'No':>12}")
    print(f"  {'Final key length':<30} {result_clean['final_key_length']:>10} b {result_eve['final_key_length']:>10} b")
    print(f"  {'Keys match':<30} {'Yes' if result_clean['keys_match'] else 'No':>12} {'Yes' if result_eve['keys_match'] else 'No':>12}")

    print(f"\n  BB84 guarantees that eavesdropping is detectable.")
    print(f"  This is information-theoretic security — no computational")
    print(f"  assumption can be broken, not even by a quantum computer.")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
