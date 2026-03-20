#!/usr/bin/env python3
"""
Benchmark Data Generator
=========================

Generates real benchmark data by running ML-KEM and ML-DSA operations
at all parameter sets and recording timing measurements.

This replaces the original synthetic 3-row CSV with actual measurements
from your hardware. The generated CSV is used by the AI analysis scripts
in ``ai/``.

Usage
-----
    python scripts/generate_benchmarks.py
    python scripts/generate_benchmarks.py --iterations 50
    python scripts/generate_benchmarks.py --output data/encryption_times.csv
"""

import argparse
import os
import sys
import time

import pandas as pd


def time_operation(func, *args, iterations: int = 20, **kwargs) -> float:
    """Time a function over multiple iterations and return average in seconds."""
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    return sum(times) / len(times), result


def benchmark_kyber(iterations: int = 20) -> list:
    """Benchmark ML-KEM (Kyber) at all parameter sets."""
    from kyber_py.kyber import Kyber512, Kyber768, Kyber1024

    results = []
    for name, cls, lattice_size in [
        ("ML-KEM-512", Kyber512, 512),
        ("ML-KEM-768", Kyber768, 768),
        ("ML-KEM-1024", Kyber1024, 1024),
    ]:
        print(f"  Benchmarking {name} ({iterations} iterations)...")

        # Key generation
        keygen_time, (pk, sk) = time_operation(cls.keygen, iterations=iterations)

        # Encapsulation
        encaps_time, (ss, ct) = time_operation(cls.encaps, pk, iterations=iterations)

        # Decapsulation
        decaps_time, _ = time_operation(cls.decaps, sk, ct, iterations=iterations)

        results.append({
            "algorithm": name,
            "lattice_size": lattice_size,
            "keygen_time": round(keygen_time, 6),
            "encryption_time": round(encaps_time, 6),
            "decryption_time": round(decaps_time, 6),
            "pk_bytes": len(pk),
            "sk_bytes": len(sk),
            "ct_bytes": len(ct),
        })

    return results


def benchmark_dilithium(iterations: int = 20) -> list:
    """Benchmark ML-DSA (Dilithium) at all parameter sets."""
    from dilithium_py.dilithium import Dilithium2, Dilithium3, Dilithium5

    message = b"Benchmark message for ML-DSA timing measurements."
    results = []

    for name, cls, lattice_size in [
        ("ML-DSA-44", Dilithium2, 512),
        ("ML-DSA-65", Dilithium3, 768),
        ("ML-DSA-87", Dilithium5, 1024),
    ]:
        print(f"  Benchmarking {name} ({iterations} iterations)...")

        # Key generation
        keygen_time, (pk, sk) = time_operation(cls.keygen, iterations=iterations)

        # Signing
        sign_time, sig = time_operation(cls.sign, sk, message, iterations=iterations)

        # Verification
        verify_time, _ = time_operation(cls.verify, pk, message, sig, iterations=iterations)

        results.append({
            "algorithm": name,
            "lattice_size": lattice_size,
            "keygen_time": round(keygen_time, 6),
            "encryption_time": round(sign_time, 6),   # "encryption" = sign for signatures
            "decryption_time": round(verify_time, 6),  # "decryption" = verify for signatures
            "pk_bytes": len(pk),
            "sk_bytes": len(sk),
            "sig_bytes": len(sig),
        })

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Generate benchmark data for PQC algorithms."
    )
    parser.add_argument(
        "--iterations", "-n", type=int, default=20,
        help="Number of iterations per measurement. Default: 20",
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None,
        help="Output CSV path. Default: data/encryption_times.csv",
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_output = os.path.join(script_dir, "..", "data", "encryption_times.csv")
    output_path = args.output or default_output

    print("=" * 60)
    print("  PQC Benchmark Data Generator")
    print("=" * 60)
    print(f"  Iterations per measurement: {args.iterations}")
    print()

    # Run benchmarks
    kem_results = benchmark_kyber(args.iterations)
    dsa_results = benchmark_dilithium(args.iterations)

    # Combine into a single DataFrame
    # Keep the original CSV schema (lattice_size, encryption_time, keygen_time, decryption_time)
    # for backward compatibility with the AI scripts, plus extra columns.
    all_results = kem_results + dsa_results
    df = pd.DataFrame(all_results)

    # Save
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n  Saved {len(df)} rows to: {output_path}")
    print()

    # Display
    print(df.to_string(index=False))
    print()


if __name__ == "__main__":
    main()
