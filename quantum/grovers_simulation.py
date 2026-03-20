#!/usr/bin/env python3
"""
Grover's Search Algorithm — Educational Simulation
===================================================

This module simulates Grover's quantum search algorithm using only NumPy
(no Qiskit dependency required). It is designed to teach how Grover's
algorithm works and why it matters for cryptography.

Why Grover's matters for cryptography
--------------------------------------
Grover's algorithm searches an unsorted database of N items in O(sqrt(N))
steps, compared to O(N) classically. For symmetric cryptography, this
means:

- A 128-bit AES key has 2^128 possible values.
- Classical brute force: 2^128 operations (infeasible).
- Grover's search: 2^64 operations (feasible for a large quantum computer).

This is why NIST recommends doubling symmetric key lengths (AES-256
instead of AES-128) in a post-quantum world. It does NOT break symmetric
crypto — it halves the effective key length.

How the algorithm works
-----------------------
1. **Initialization:** Put n qubits into an equal superposition of all
   2^n basis states using Hadamard gates.

2. **Oracle:** Flip the phase of the target state(s). This is the
   "black box" that recognizes the answer.

3. **Diffusion (Grover operator):** Reflect all amplitudes about the
   mean amplitude. This amplifies the marked state and suppresses
   the rest.

4. **Repeat** steps 2-3 approximately pi/4 * sqrt(N) times.

5. **Measure:** The target state now has high probability.

This simulation
---------------
We simulate the algorithm with n qubits (configurable, default 3) and
a single marked target state. The script:

- Prints the probability of each state after each Grover iteration
- Shows how the target state's probability grows toward 1.0
- Saves a bar chart of the final probability distribution
- Reports the optimal number of iterations

Dependencies
------------
    pip install numpy matplotlib

Usage
-----
    python quantum/grovers_simulation.py
    python quantum/grovers_simulation.py --qubits 4 --target 5
"""

import argparse
import math
import os
import sys

import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend for saving figures
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


# ─── Quantum Gate Primitives ────────────────────────────────────────────────

def hadamard_n(n: int) -> np.ndarray:
    """Construct the n-qubit Hadamard gate (H^{tensor n}).

    The Hadamard gate on one qubit is:
        H = 1/sqrt(2) * [[1,  1],
                          [1, -1]]

    The n-qubit version is the tensor (Kronecker) product of n copies.
    """
    H1 = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    H_n = H1
    for _ in range(n - 1):
        H_n = np.kron(H_n, H1)
    return H_n


def oracle(n: int, target: int) -> np.ndarray:
    """Construct the oracle matrix that flips the phase of the target state.

    The oracle is a diagonal matrix where every entry is +1 except the
    target state, which is -1. In a real quantum computer, this oracle
    would be a reversible circuit that recognizes the answer.

    Args:
        n:      Number of qubits (search space has 2^n states).
        target: Index of the marked state (0 to 2^n - 1).
    """
    N = 2 ** n
    O = np.eye(N, dtype=complex)
    O[target, target] = -1
    return O


def diffusion(n: int) -> np.ndarray:
    """Construct the Grover diffusion operator (2|s><s| - I).

    |s> is the uniform superposition state. The diffusion operator
    reflects all amplitudes about the mean, amplifying states with
    above-average amplitude and suppressing the rest.

    This is equivalent to: H^n (2|0><0| - I) H^n
    """
    N = 2 ** n
    H_n = hadamard_n(n)

    # |0><0| projector in computational basis
    zero_proj = np.zeros((N, N), dtype=complex)
    zero_proj[0, 0] = 1

    # 2|0><0| - I
    inner = 2 * zero_proj - np.eye(N, dtype=complex)

    # H^n (2|0><0| - I) H^n
    return H_n @ inner @ H_n


def optimal_iterations(n: int) -> int:
    """Calculate the optimal number of Grover iterations.

    For a single marked item in a search space of N = 2^n items,
    the optimal count is floor(pi/4 * sqrt(N)).
    """
    N = 2 ** n
    return max(1, int(math.floor(math.pi / 4 * math.sqrt(N))))


# ─── Simulation ─────────────────────────────────────────────────────────────

def run_grovers(n: int, target: int, verbose: bool = True) -> np.ndarray:
    """Simulate Grover's algorithm and return the final state vector.

    Args:
        n:       Number of qubits.
        target:  Index of the marked state (0 to 2^n - 1).
        verbose: If True, print probabilities after each iteration.

    Returns:
        The final state vector as a 1-D complex numpy array.
    """
    N = 2 ** n
    if target < 0 or target >= N:
        raise ValueError(f"Target {target} is out of range for {n} qubits (0 to {N-1}).")

    num_iters = optimal_iterations(n)

    if verbose:
        print(f"\n  Qubits:             {n}")
        print(f"  Search space:       {N} states")
        print(f"  Target state:       |{target:0{n}b}> (decimal {target})")
        print(f"  Optimal iterations: {num_iters}")
        print(f"  Classical lookups:  {N} (worst case)")
        print(f"  Grover speedup:     ~{N / num_iters:.1f}x")

    # Step 1: Initialize uniform superposition
    H_n = hadamard_n(n)
    state = np.zeros(N, dtype=complex)
    state[0] = 1.0  # |00...0>
    state = H_n @ state

    # Build operators
    O = oracle(n, target)
    D = diffusion(n)

    # Steps 2-4: Apply Grover iterations
    for i in range(num_iters):
        state = O @ state   # Oracle: flip phase of target
        state = D @ state   # Diffusion: amplify target

        if verbose:
            probs = np.abs(state) ** 2
            target_prob = probs[target]
            print(f"\n  After iteration {i + 1}:")
            print(f"    P(target |{target:0{n}b}>) = {target_prob:.4f}")
            if n <= 4:
                # Print all probabilities for small search spaces
                for j in range(N):
                    marker = " <-- TARGET" if j == target else ""
                    print(f"    |{j:0{n}b}>: {probs[j]:.4f}{marker}")

    return state


def plot_probabilities(n: int, target: int, state: np.ndarray, save_path: str) -> None:
    """Save a bar chart of the final probability distribution.

    Args:
        n:         Number of qubits.
        target:    Index of the marked state.
        state:     Final state vector.
        save_path: File path to save the chart.
    """
    if not HAS_MATPLOTLIB:
        print(f"\n  matplotlib not installed -- skipping chart.")
        return

    N = 2 ** n
    probs = np.abs(state) ** 2
    labels = [f"|{j:0{n}b}>" for j in range(N)]
    colors = ["#e74c3c" if j == target else "#3498db" for j in range(N)]

    fig, ax = plt.subplots(figsize=(max(6, N * 0.6), 4))
    ax.bar(range(N), probs, color=colors, edgecolor="white", linewidth=0.5)
    ax.set_xticks(range(N))
    ax.set_xticklabels(labels, rotation=45 if N > 8 else 0, fontsize=8)
    ax.set_ylabel("Probability")
    ax.set_title(f"Grover's Algorithm -- {n} qubits, target |{target:0{n}b}>")
    ax.set_ylim(0, 1.05)
    ax.axhline(y=1/N, color="gray", linestyle="--", linewidth=0.8, label=f"Uniform = {1/N:.3f}")
    ax.legend()
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    print(f"\n  Chart saved to: {save_path}")


# ─── CLI Entry Point ────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulate Grover's quantum search algorithm."
    )
    parser.add_argument(
        "--qubits", "-n", type=int, default=3,
        help="Number of qubits (search space = 2^n). Default: 3",
    )
    parser.add_argument(
        "--target", "-t", type=int, default=None,
        help="Index of the marked state (0 to 2^n - 1). Default: random",
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None,
        help="Path to save the probability chart. Default: grovers_result.png",
    )
    args = parser.parse_args()

    n = args.qubits
    if n < 1 or n > 10:
        print("Error: qubits must be between 1 and 10.")
        sys.exit(1)

    N = 2 ** n
    target = args.target
    if target is None:
        target = np.random.randint(0, N)

    if target < 0 or target >= N:
        print(f"Error: target must be between 0 and {N - 1}.")
        sys.exit(1)

    output = args.output or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "grovers_result.png"
    )

    print("=" * 60)
    print("  Grover's Search Algorithm Simulation")
    print("=" * 60)

    state = run_grovers(n, target, verbose=True)

    # Final measurement probabilities
    probs = np.abs(state) ** 2
    target_prob = probs[target]

    print(f"\n{'=' * 60}")
    print(f"  Result: P(target) = {target_prob:.4f}")
    print(f"  A measurement would find the target with ~{target_prob*100:.1f}% probability.")
    print(f"{'=' * 60}")

    plot_probabilities(n, target, state, output)


# Keep backward compatibility: the old function name still works.
def grovers_algorithm():
    """Legacy entry point -- runs a 3-qubit demo with target state 5."""
    state = run_grovers(3, target=5, verbose=True)
    probs = np.abs(state) ** 2
    print(f"\nFinal probabilities: {probs}")


if __name__ == "__main__":
    main()
