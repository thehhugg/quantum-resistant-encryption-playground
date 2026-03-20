#!/usr/bin/env python3
"""
Shor's Algorithm — Educational Simulation
==========================================

This module demonstrates the core ideas behind Shor's factoring algorithm,
the quantum algorithm that threatens RSA, Diffie-Hellman, and elliptic-curve
cryptography.

Why Shor's matters for cryptography
------------------------------------
RSA security relies on the assumption that factoring large numbers is hard.
The best known classical algorithm (General Number Field Sieve) runs in
sub-exponential time. Shor's algorithm factors an n-bit integer in
O(n^3) time on a quantum computer — exponentially faster.

If a sufficiently large, fault-tolerant quantum computer is built, it
could factor the 2048-bit numbers used in RSA in hours instead of
billions of years. This is the primary motivation for post-quantum
cryptography.

What this script demonstrates
------------------------------
Shor's algorithm has two parts:

1. **Classical reduction:** Reduce factoring to finding the *period* of
   a modular exponentiation function f(x) = a^x mod N.

2. **Quantum period-finding:** Use the Quantum Fourier Transform (QFT)
   to find the period efficiently.

This simulation implements both parts:
- The classical reduction (choosing a, computing gcd, etc.)
- A simulated quantum period-finding step (we compute the period by
  simulating the quantum state evolution with NumPy, not on real
  quantum hardware)

We factor small numbers (up to ~1000) to keep the simulation tractable.
The algorithm and math are identical to what would run on a real quantum
computer — only the execution substrate differs.

Dependencies
------------
    pip install numpy

Usage
-----
    python quantum/shors_simulation.py
    python quantum/shors_simulation.py --number 91
    python quantum/shors_simulation.py --number 15 --verbose
"""

import argparse
import math
import sys
from typing import Optional

import numpy as np


# ─── Classical Helpers ──────────────────────────────────────────────────────

def is_prime(n: int) -> bool:
    """Check if n is prime using trial division."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def is_prime_power(n: int) -> bool:
    """Check if n is a prime power (p^k for some prime p and k >= 2)."""
    for p in range(2, int(math.isqrt(n)) + 1):
        if n % p == 0:
            k = n
            while k % p == 0:
                k //= p
            if k == 1:
                return True
            return False
    return False


def classical_order_finding(a: int, N: int) -> int:
    """Find the order of a modulo N by brute force.

    The order r is the smallest positive integer such that a^r = 1 (mod N).
    On a real quantum computer, this is the step replaced by quantum
    period-finding using the QFT.
    """
    if math.gcd(a, N) != 1:
        raise ValueError(f"gcd({a}, {N}) != 1; a must be coprime to N.")
    r = 1
    current = a % N
    while current != 1:
        current = (current * a) % N
        r += 1
        if r > N:
            raise RuntimeError(f"Order not found for a={a}, N={N}")
    return r


def simulated_quantum_order_finding(a: int, N: int, verbose: bool = False) -> int:
    """Simulate the quantum period-finding subroutine.

    In a real quantum computer, this would:
    1. Prepare two registers in superposition
    2. Apply modular exponentiation as a controlled unitary
    3. Apply the inverse QFT to the first register
    4. Measure to get a value close to s/r (for some integer s)
    5. Use continued fractions to extract r

    Here we simulate the state vector evolution directly with NumPy.
    For tractability, we limit the register size.

    Args:
        a:       Base for modular exponentiation.
        N:       Number to factor.
        verbose: If True, print intermediate steps.

    Returns:
        The period r of a^x mod N.
    """
    # Choose register sizes
    # The "counting register" needs enough qubits to resolve the period.
    # We use 2*ceil(log2(N)) qubits, as in the standard algorithm.
    n_count = 2 * math.ceil(math.log2(N))
    Q = 2 ** n_count  # Number of states in counting register

    if verbose:
        print(f"    Counting register: {n_count} qubits ({Q} states)")

    # Step 1: Build the function f(x) = a^x mod N for x in [0, Q)
    # In a real quantum computer, this is a reversible circuit.
    f_values = np.zeros(Q, dtype=int)
    f_values[0] = 1
    for x in range(1, Q):
        f_values[x] = (f_values[x - 1] * a) % N

    # Step 2: Simulate the QFT measurement
    # After applying the controlled modular exponentiation and inverse QFT,
    # measuring the counting register yields a value close to s * Q / r
    # for a random integer s in [0, r).
    #
    # We simulate this by computing the DFT of the indicator function
    # for states where f(x) equals some observed value.

    # Pick an arbitrary observed value (the "collapse" of the work register)
    observed = f_values[0]  # Could be any value; we pick f(0) = 1
    indicator = (f_values == observed).astype(complex)

    # Normalize
    norm = np.sqrt(np.sum(np.abs(indicator) ** 2))
    if norm > 0:
        indicator /= norm

    # Apply DFT (simulating inverse QFT + measurement)
    spectrum = np.fft.fft(indicator)
    probabilities = np.abs(spectrum) ** 2
    probabilities /= probabilities.sum()

    # Step 3: Sample from the distribution and extract the period
    # In practice, we'd repeat this several times. Here we try the
    # top peaks.
    peak_indices = np.argsort(probabilities)[::-1]

    for idx in peak_indices[:10]:
        if idx == 0:
            continue  # s=0 gives no information

        # The measured value is approximately s * Q / r
        # Use continued fractions to find r
        measured_phase = idx / Q

        # Continued fraction expansion to find r
        r_candidate = _convergent_denominator(measured_phase, N)

        if r_candidate and r_candidate > 0 and pow(a, r_candidate, N) == 1:
            if verbose:
                print(f"    Measured peak at index {idx}, phase ~ {measured_phase:.6f}")
                print(f"    Extracted period candidate: r = {r_candidate}")
            return r_candidate

    # Fallback: classical computation (would not happen on ideal hardware)
    if verbose:
        print("    Quantum simulation did not converge; using classical fallback.")
    return classical_order_finding(a, N)


def _convergent_denominator(phase: float, max_denom: int) -> Optional[int]:
    """Extract the denominator from the continued fraction expansion of phase.

    This is the classical post-processing step in Shor's algorithm.
    Given a measured phase ~ s/r, we find r using continued fractions.
    """
    # Simple continued fraction expansion
    a0 = phase
    denominators = []
    h_prev, h_curr = 0, 1
    k_prev, k_curr = 1, 0

    for _ in range(50):  # Max iterations
        if abs(a0) < 1e-10:
            break
        a_int = int(round(1.0 / a0))
        if a_int == 0:
            break

        h_prev, h_curr = h_curr, a_int * h_curr + h_prev
        k_prev, k_curr = k_curr, a_int * k_curr + k_prev

        if k_curr > max_denom:
            break

        denominators.append(k_curr)
        a0 = 1.0 / a0 - a_int

        if abs(a0) < 1e-10:
            break

    # Return the largest denominator that doesn't exceed N
    for d in reversed(denominators):
        if 0 < d <= max_denom:
            return d
    return None


# ─── Shor's Algorithm ──────────────────────────────────────────────────────

def shors_algorithm(N: int, verbose: bool = False) -> tuple:
    """Run Shor's algorithm to factor N.

    Args:
        N:       The composite number to factor.
        verbose: If True, print detailed steps.

    Returns:
        A tuple (p, q) such that p * q = N, or None if factoring fails.
    """
    if verbose:
        print(f"\n  Factoring N = {N}")
        print(f"  {'─' * 50}")

    # ── Pre-checks ───────────────────────────────────────────────────────
    if N < 2:
        print(f"  {N} is too small to factor.")
        return None

    if N % 2 == 0:
        if verbose:
            print(f"  N is even. Trivial factor: 2")
        return (2, N // 2)

    if is_prime(N):
        if verbose:
            print(f"  N = {N} is prime. Cannot factor.")
        return None

    if is_prime_power(N):
        if verbose:
            print(f"  N = {N} is a prime power. Finding base...")
        for p in range(2, int(math.isqrt(N)) + 1):
            k = round(math.log(N) / math.log(p))
            if p ** k == N:
                if verbose:
                    print(f"  N = {p}^{k}")
                return (p, N // p)

    # ── Main loop: choose random a, find period, extract factors ─────────
    max_attempts = 20
    for attempt in range(1, max_attempts + 1):
        # Step 1: Choose a random a in [2, N-1]
        a = np.random.randint(2, N)

        if verbose:
            print(f"\n  Attempt {attempt}: a = {a}")

        # Step 2: Check if gcd(a, N) > 1 (lucky case)
        g = math.gcd(a, N)
        if g > 1:
            if verbose:
                print(f"  Lucky! gcd({a}, {N}) = {g}")
            return (g, N // g)

        # Step 3: Find the order r of a modulo N (quantum step)
        if verbose:
            print(f"  Finding order of {a} mod {N} (quantum period-finding)...")

        r = simulated_quantum_order_finding(a, N, verbose=verbose)

        if verbose:
            print(f"  Order r = {r}")

        # Step 4: Check if r is useful
        if r % 2 != 0:
            if verbose:
                print(f"  r is odd — trying another a.")
            continue

        # Step 5: Compute candidate factors
        x = pow(a, r // 2, N)
        if x == N - 1:
            if verbose:
                print(f"  a^(r/2) = -1 (mod N) — trying another a.")
            continue

        p = math.gcd(x + 1, N)
        q = math.gcd(x - 1, N)

        if verbose:
            print(f"  a^(r/2) mod N = {x}")
            print(f"  gcd({x}+1, {N}) = {p}")
            print(f"  gcd({x}-1, {N}) = {q}")

        # Check if we found non-trivial factors
        if 1 < p < N:
            return (p, N // p)
        if 1 < q < N:
            return (q, N // q)

        if verbose:
            print(f"  No non-trivial factor found — trying another a.")

    if verbose:
        print(f"\n  Failed to factor {N} after {max_attempts} attempts.")
    return None


# ─── CLI Entry Point ────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulate Shor's quantum factoring algorithm."
    )
    parser.add_argument(
        "--number", "-N", type=int, default=None,
        help="The composite number to factor. Default: demo sequence.",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Print detailed steps of the algorithm.",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  Shor's Factoring Algorithm Simulation")
    print("=" * 60)
    print()
    print("  Shor's algorithm factors integers in polynomial time on a")
    print("  quantum computer. This breaks RSA, Diffie-Hellman, and ECC.")
    print("  Post-quantum cryptography exists to resist this threat.")
    print()
    print("  This simulation uses NumPy to simulate the quantum state")
    print("  evolution. The math is identical to real Shor's; only the")
    print("  execution substrate differs.")

    if args.number is not None:
        # Factor a single number
        result = shors_algorithm(args.number, verbose=args.verbose)
        if result:
            p, q = result
            print(f"\n  Result: {args.number} = {p} x {q}")
            assert p * q == args.number
        else:
            print(f"\n  Could not factor {args.number}.")
    else:
        # Demo: factor several numbers
        demo_numbers = [15, 21, 35, 77, 91, 143, 221, 323, 437, 667]
        print(f"\n  Demo: factoring {len(demo_numbers)} composite numbers")
        print(f"  {'─' * 50}")

        results = []
        for N in demo_numbers:
            result = shors_algorithm(N, verbose=args.verbose)
            if result:
                p, q = sorted(result)
                assert p * q == N
                results.append((N, p, q, "OK"))
                print(f"  {N:>6} = {p} x {q}")
            else:
                results.append((N, None, None, "FAIL"))
                print(f"  {N:>6} — factoring failed")

        # Summary table
        successes = sum(1 for _, _, _, s in results if s == "OK")
        print(f"\n  {'─' * 50}")
        print(f"  Factored {successes}/{len(demo_numbers)} numbers successfully.")

    # Cryptographic context
    print(f"\n{'=' * 60}")
    print("  Cryptographic Implications")
    print(f"{'=' * 60}")
    print()
    print("  RSA-2048 uses a 2048-bit modulus (product of two ~1024-bit primes).")
    print("  Classical factoring: ~2^112 operations (infeasible).")
    print("  Shor's algorithm:    ~2048^3 ~ 10^10 operations (feasible).")
    print()
    print("  A quantum computer with ~4000 logical qubits could break RSA-2048.")
    print("  This is why NIST standardized ML-KEM and ML-DSA as replacements.")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
