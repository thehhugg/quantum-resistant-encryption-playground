#!/usr/bin/env python3
"""
Interactive Benchmark Runner
=============================

A user-friendly script that lets you choose which PQC algorithms to
benchmark, how many iterations to run, and displays results with
optional chart output.

Usage
-----
    python scripts/benchmark_runner.py                  # Interactive mode
    python scripts/benchmark_runner.py --all            # Benchmark everything
    python scripts/benchmark_runner.py --kem            # ML-KEM only
    python scripts/benchmark_runner.py --dsa            # ML-DSA only
    python scripts/benchmark_runner.py --all --chart    # With chart output
    python scripts/benchmark_runner.py --all -n 50      # 50 iterations
"""

import argparse
import os
import sys
import time

import numpy as np

# ─── Benchmark Functions ─────────────────────────────────────────────────────

def _time_op(func, *args, iterations: int = 20):
    """Time a function and return (result, avg_seconds, std_seconds)."""
    times = []
    result = None
    for _ in range(iterations):
        start = time.perf_counter()
        result = func(*args)
        times.append(time.perf_counter() - start)
    return result, np.mean(times), np.std(times)


def benchmark_kem(iterations: int = 20) -> list:
    """Benchmark all ML-KEM parameter sets."""
    from kyber_py.kyber import Kyber512, Kyber768, Kyber1024

    results = []
    for name, cls in [("ML-KEM-512", Kyber512), ("ML-KEM-768", Kyber768), ("ML-KEM-1024", Kyber1024)]:
        print(f"    {name}...", end=" ", flush=True)

        (pk, sk), kg_avg, kg_std = _time_op(cls.keygen, iterations=iterations)
        (ss, ct), enc_avg, enc_std = _time_op(cls.encaps, pk, iterations=iterations)
        _, dec_avg, dec_std = _time_op(cls.decaps, sk, ct, iterations=iterations)

        results.append({
            "algorithm": name,
            "type": "KEM",
            "pk_bytes": len(pk),
            "sk_bytes": len(sk),
            "ct_bytes": len(ct),
            "keygen_ms": kg_avg * 1000,
            "keygen_std": kg_std * 1000,
            "encaps_ms": enc_avg * 1000,
            "encaps_std": enc_std * 1000,
            "decaps_ms": dec_avg * 1000,
            "decaps_std": dec_std * 1000,
        })
        print(f"done ({kg_avg*1000:.1f} / {enc_avg*1000:.1f} / {dec_avg*1000:.1f} ms)")

    return results


def benchmark_dsa(iterations: int = 20) -> list:
    """Benchmark all ML-DSA parameter sets."""
    from dilithium_py.dilithium import Dilithium2, Dilithium3, Dilithium5

    msg = b"Benchmark message for ML-DSA timing."
    results = []

    for name, cls in [("ML-DSA-44", Dilithium2), ("ML-DSA-65", Dilithium3), ("ML-DSA-87", Dilithium5)]:
        print(f"    {name}...", end=" ", flush=True)

        (pk, sk), kg_avg, kg_std = _time_op(cls.keygen, iterations=iterations)
        sig, sign_avg, sign_std = _time_op(cls.sign, sk, msg, iterations=iterations)
        _, ver_avg, ver_std = _time_op(cls.verify, pk, msg, sig, iterations=iterations)

        results.append({
            "algorithm": name,
            "type": "Signature",
            "pk_bytes": len(pk),
            "sk_bytes": len(sk),
            "sig_bytes": len(sig),
            "keygen_ms": kg_avg * 1000,
            "keygen_std": kg_std * 1000,
            "sign_ms": sign_avg * 1000,
            "sign_std": sign_std * 1000,
            "verify_ms": ver_avg * 1000,
            "verify_std": ver_std * 1000,
        })
        print(f"done ({kg_avg*1000:.1f} / {sign_avg*1000:.1f} / {ver_avg*1000:.1f} ms)")

    return results


# ─── Display ─────────────────────────────────────────────────────────────────

def print_kem_results(results: list, iterations: int):
    """Print KEM benchmark results."""
    print(f"\n  ML-KEM Key Encapsulation ({iterations} iterations each)")
    print(f"  {'Algorithm':<14} {'PK':>8} {'SK':>8} {'CT':>8} {'KeyGen':>12} {'Encaps':>12} {'Decaps':>12}")
    print(f"  {'-'*14} {'-'*8} {'-'*8} {'-'*8} {'-'*12} {'-'*12} {'-'*12}")
    for r in results:
        print(f"  {r['algorithm']:<14} {r['pk_bytes']:>6} B {r['sk_bytes']:>6} B {r['ct_bytes']:>6} B "
              f"{r['keygen_ms']:>7.2f}ms    {r['encaps_ms']:>7.2f}ms    {r['decaps_ms']:>7.2f}ms")


def print_dsa_results(results: list, iterations: int):
    """Print DSA benchmark results."""
    print(f"\n  ML-DSA Digital Signatures ({iterations} iterations each)")
    print(f"  {'Algorithm':<14} {'PK':>8} {'SK':>8} {'Sig':>8} {'KeyGen':>12} {'Sign':>12} {'Verify':>12}")
    print(f"  {'-'*14} {'-'*8} {'-'*8} {'-'*8} {'-'*12} {'-'*12} {'-'*12}")
    for r in results:
        print(f"  {r['algorithm']:<14} {r['pk_bytes']:>6} B {r['sk_bytes']:>6} B {r['sig_bytes']:>6} B "
              f"{r['keygen_ms']:>7.2f}ms    {r['sign_ms']:>7.2f}ms    {r['verify_ms']:>7.2f}ms")


def save_chart(kem_results: list, dsa_results: list, path: str):
    """Save a benchmark comparison chart."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # KEM chart
    if kem_results:
        ax = axes[0]
        names = [r["algorithm"] for r in kem_results]
        x = np.arange(len(names))
        w = 0.25
        ax.bar(x - w, [r["keygen_ms"] for r in kem_results], w,
               yerr=[r["keygen_std"] for r in kem_results],
               label="KeyGen", color="steelblue", capsize=3)
        ax.bar(x, [r["encaps_ms"] for r in kem_results], w,
               yerr=[r["encaps_std"] for r in kem_results],
               label="Encaps", color="coral", capsize=3)
        ax.bar(x + w, [r["decaps_ms"] for r in kem_results], w,
               yerr=[r["decaps_std"] for r in kem_results],
               label="Decaps", color="seagreen", capsize=3)
        ax.set_xticks(x)
        ax.set_xticklabels(names)
        ax.set_ylabel("Time (ms)")
        ax.set_title("ML-KEM Benchmarks")
        ax.legend()
        ax.grid(True, alpha=0.3, axis="y")

    # DSA chart
    if dsa_results:
        ax = axes[1]
        names = [r["algorithm"] for r in dsa_results]
        x = np.arange(len(names))
        w = 0.25
        ax.bar(x - w, [r["keygen_ms"] for r in dsa_results], w,
               yerr=[r["keygen_std"] for r in dsa_results],
               label="KeyGen", color="steelblue", capsize=3)
        ax.bar(x, [r["sign_ms"] for r in dsa_results], w,
               yerr=[r["sign_std"] for r in dsa_results],
               label="Sign", color="coral", capsize=3)
        ax.bar(x + w, [r["verify_ms"] for r in dsa_results], w,
               yerr=[r["verify_std"] for r in dsa_results],
               label="Verify", color="seagreen", capsize=3)
        ax.set_xticks(x)
        ax.set_xticklabels(names)
        ax.set_ylabel("Time (ms)")
        ax.set_title("ML-DSA Benchmarks")
        ax.legend()
        ax.grid(True, alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"\n  Chart saved to: {path}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Interactive PQC benchmark runner."
    )
    parser.add_argument("--kem", action="store_true", help="Benchmark ML-KEM only")
    parser.add_argument("--dsa", action="store_true", help="Benchmark ML-DSA only")
    parser.add_argument("--all", action="store_true", help="Benchmark everything")
    parser.add_argument("-n", "--iterations", type=int, default=20,
                        help="Iterations per measurement (default: 20)")
    parser.add_argument("--chart", type=str, nargs="?", const="benchmark_results.png",
                        help="Save chart to file (default: benchmark_results.png)")
    args = parser.parse_args()

    # If no flags specified, run everything
    if not (args.kem or args.dsa or args.all):
        args.all = True

    run_kem = args.kem or args.all
    run_dsa = args.dsa or args.all

    print("=" * 70)
    print("  PQC Benchmark Runner")
    print("=" * 70)
    print(f"  Iterations: {args.iterations}")
    print(f"  Algorithms: {'ML-KEM' if run_kem else ''} {'ML-DSA' if run_dsa else ''}")
    print()

    kem_results = []
    dsa_results = []

    if run_kem:
        print("  Running ML-KEM benchmarks...")
        kem_results = benchmark_kem(args.iterations)
        print_kem_results(kem_results, args.iterations)

    if run_dsa:
        print("\n  Running ML-DSA benchmarks...")
        dsa_results = benchmark_dsa(args.iterations)
        print_dsa_results(dsa_results, args.iterations)

    if args.chart:
        save_chart(kem_results, dsa_results, args.chart)

    print(f"\n{'=' * 70}\n")


if __name__ == "__main__":
    main()
