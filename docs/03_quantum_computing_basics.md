# Quantum Computing Basics for Cryptographers

This document covers just enough quantum computing to understand why Shor's and Grover's algorithms threaten classical cryptography. You do not need to understand quantum mechanics to follow this.

## Qubits and Superposition

A classical bit is either 0 or 1. A qubit can be in a **superposition** of both states simultaneously. We write the state of a qubit as:

    |psi> = alpha * |0> + beta * |1>

where alpha and beta are complex numbers called **amplitudes**, and |alpha|^2 + |beta|^2 = 1.

When you **measure** a qubit, it collapses to |0> with probability |alpha|^2 or to |1> with probability |beta|^2. The superposition is destroyed.

With n qubits, you can represent a superposition of all 2^n possible states simultaneously. This is the source of quantum computing's power — and its subtlety.

## Quantum Gates

Quantum gates are operations that transform qubit states. They are represented by unitary matrices. Key gates:

- **Hadamard (H):** Puts a qubit into equal superposition. H|0> = (|0> + |1>)/sqrt(2).
- **CNOT:** A two-qubit gate that flips the second qubit if the first is |1>. Creates entanglement.
- **Phase gates:** Rotate the phase of a qubit's amplitude without changing measurement probabilities.

A quantum algorithm is a sequence of gates applied to qubits, followed by measurement.

## Grover's Algorithm

**Problem:** Given a function f(x) that returns 1 for exactly one input x* out of N possibilities, find x*.

**Classical:** Check each input one by one. Expected time: N/2 evaluations.

**Grover's:** Find x* in approximately sqrt(N) evaluations.

**How it works:**

1. Start with all N states in equal superposition (each has amplitude 1/sqrt(N)).
2. **Oracle step:** Flip the sign of the amplitude of the target state x*.
3. **Diffusion step:** Reflect all amplitudes about the mean. This increases the amplitude of x* and decreases the rest.
4. Repeat steps 2-3 about (pi/4) * sqrt(N) times.
5. Measure. The target state x* has high probability.

**Cryptographic impact:** For a 128-bit symmetric key, classical brute force takes 2^128 operations. Grover's takes 2^64 — still a lot, but within reach of a large quantum computer. Solution: use 256-bit keys.

Try it: `python quantum/grovers_simulation.py --qubits 4 --target 7`

## Shor's Algorithm

**Problem:** Given a composite integer N, find its prime factors.

**Classical:** The best algorithm (General Number Field Sieve) runs in sub-exponential time. For RSA-2048, this is approximately 2^112 operations — infeasible.

**Shor's:** Factor N in O(n^3) time, where n is the number of bits. For RSA-2048, this is about 10^10 operations — feasible.

**How it works:**

1. **Classical reduction:** Factoring N is equivalent to finding the **period** r of the function f(x) = a^x mod N for a random a coprime to N.

2. **Quantum period-finding:** Prepare two quantum registers. Apply modular exponentiation as a quantum operation. Apply the **Quantum Fourier Transform** (QFT) to the first register. Measure to get a value close to s/r for some integer s.

3. **Classical post-processing:** Use the continued fraction algorithm to extract r from the measured value. Then compute gcd(a^(r/2) + 1, N) and gcd(a^(r/2) - 1, N) to get the factors.

**Why it works:** The QFT efficiently extracts the period of a periodic function encoded in quantum amplitudes. This is something no known classical algorithm can do efficiently.

**Cryptographic impact:** Shor's algorithm breaks RSA, Diffie-Hellman, and elliptic curve cryptography. This is the primary motivation for post-quantum cryptography.

Try it: `python quantum/shors_simulation.py --number 91 --verbose`

## What Quantum Computers Cannot Do

Common misconceptions:

- **Quantum computers do NOT try all answers simultaneously.** Superposition lets you set up interference patterns, but you can only extract one answer per measurement. The art is in making the right answer have high probability.

- **Quantum computers do NOT break all encryption.** They break specific mathematical problems (factoring, discrete log). Symmetric encryption (AES) and hash functions are only mildly affected (Grover's halves the key length).

- **Quantum computers do NOT break lattice-based crypto.** The best known quantum algorithms for lattice problems provide only a small polynomial speedup, not the exponential speedup Shor's gives for factoring.

## Current State of Quantum Hardware (2025)

| Metric | Current State | Needed to Break RSA-2048 |
|--------|--------------|-------------------------|
| Physical qubits | ~1,000-10,000 | ~4,000,000+ |
| Logical qubits | ~10-100 | ~4,000 |
| Error rate | ~0.1-1% | ~0.001% |
| Gate fidelity | ~99-99.9% | ~99.999% |

The gap between current hardware and what is needed to break RSA is large. But the gap is closing, and "harvest now, decrypt later" attacks mean the threat is already real for long-lived secrets.

## Further Reading

- Nielsen, M. & Chuang, I. (2010). "Quantum Computation and Quantum Information." — The standard textbook.
- [IBM Quantum Learning](https://learning.quantum.ibm.com/) — Free interactive tutorials.
- [Qiskit Textbook](https://github.com/Qiskit/textbook) — Open-source quantum computing textbook.
