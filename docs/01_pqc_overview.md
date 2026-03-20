# Post-Quantum Cryptography: What It Is and Why It Matters

## The Problem

Public-key cryptography underpins nearly every secure system on the internet: TLS (HTTPS), SSH, VPNs, code signing, email encryption, and cryptocurrency. The two most widely deployed families of public-key algorithms are:

- **RSA** — security based on the difficulty of factoring large integers.
- **Elliptic Curve Cryptography (ECC)** — security based on the difficulty of the elliptic curve discrete logarithm problem.

Both of these problems can be solved efficiently by a quantum computer running **Shor's algorithm**. A sufficiently large, fault-tolerant quantum computer could break RSA-2048 in hours instead of billions of years.

No such computer exists today. Current quantum computers have a few thousand noisy physical qubits; breaking RSA-2048 would require roughly 4,000 *logical* (error-corrected) qubits, which translates to millions of physical qubits with current error rates. Estimates for when this threshold will be reached range from 2030 to 2050+.

## Why Act Now

Even though large-scale quantum computers are years away, there are reasons to prepare today:

1. **Harvest now, decrypt later.** Adversaries can record encrypted traffic today and decrypt it once quantum computers are available. Sensitive data with long confidentiality requirements (government, healthcare, financial) is already at risk.

2. **Migration takes time.** Upgrading cryptographic infrastructure across an organization takes years. The transition to SHA-2 from SHA-1 took over a decade.

3. **Standards are ready.** NIST finalized its first post-quantum standards in 2024 (FIPS 203, 204, 205), so there is no longer a reason to wait.

## What Post-Quantum Cryptography Is

Post-quantum cryptography (PQC) refers to cryptographic algorithms that are believed to be secure against both classical and quantum computers. These algorithms run on ordinary classical hardware — they do not require a quantum computer.

The main families of PQC algorithms are:

| Family | Hard Problem | Used For | NIST Standard |
|--------|-------------|----------|---------------|
| Lattice-based | Shortest vector / Learning With Errors | Key encapsulation, signatures | FIPS 203 (ML-KEM), FIPS 204 (ML-DSA) |
| Hash-based | Collision resistance of hash functions | Signatures | FIPS 205 (SLH-DSA) |
| Code-based | Decoding random linear codes | Key encapsulation | (HQC, under evaluation) |
| Isogeny-based | Isogenies between elliptic curves | Key encapsulation | (SIKE, broken in 2022) |

The lattice-based algorithms are the most important in practice because they offer both key encapsulation and signatures with reasonable key sizes and performance.

## The NIST Standards

NIST ran a multi-year competition (2016-2024) to select and standardize post-quantum algorithms. The results:

### FIPS 203: ML-KEM (Module-Lattice-Based Key-Encapsulation Mechanism)

Formerly known as CRYSTALS-Kyber. ML-KEM replaces RSA and ECDH for key exchange. It produces a shared secret that two parties can use as a symmetric key.

- **Parameter sets:** ML-KEM-512 (Level 1), ML-KEM-768 (Level 3), ML-KEM-1024 (Level 5)
- **Key sizes:** 800 to 1,568 bytes (public key)
- **Ciphertext:** 768 to 1,568 bytes
- **Shared secret:** 32 bytes (always)

Try it: `python examples/01_ml_kem_keygen.py`

### FIPS 204: ML-DSA (Module-Lattice-Based Digital Signature Algorithm)

Formerly known as CRYSTALS-Dilithium. ML-DSA replaces RSA and ECDSA for digital signatures.

- **Parameter sets:** ML-DSA-44 (Level 2), ML-DSA-65 (Level 3), ML-DSA-87 (Level 5)
- **Key sizes:** 1,312 to 2,592 bytes (public key)
- **Signature:** 2,420 to 4,627 bytes

Try it: `python examples/02_ml_dsa_signatures.py`

### FIPS 205: SLH-DSA (Stateless Hash-Based Digital Signature Algorithm)

Formerly known as SPHINCS+. A conservative backup signature scheme based only on hash functions. Larger signatures but relies on minimal assumptions.

## Symmetric Cryptography Is Mostly Fine

Shor's algorithm only threatens *asymmetric* (public-key) cryptography. Symmetric algorithms like AES are affected by **Grover's algorithm**, which provides a quadratic speedup for brute-force search. This halves the effective key length:

- AES-128 → 64-bit security against quantum (not enough)
- AES-256 → 128-bit security against quantum (still secure)

The practical recommendation is to use AES-256 instead of AES-128 in a post-quantum world. No new symmetric algorithms are needed.

Try it: `python quantum/grovers_simulation.py`

## Further Reading

- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [FIPS 203 (ML-KEM)](https://csrc.nist.gov/pubs/fips/203/final)
- [FIPS 204 (ML-DSA)](https://csrc.nist.gov/pubs/fips/204/final)
- [FIPS 205 (SLH-DSA)](https://csrc.nist.gov/pubs/fips/205/final)
- [Open Quantum Safe Project](https://openquantumsafe.org/)
