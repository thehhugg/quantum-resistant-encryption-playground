# Quantum-Resistant Encryption Playground

A hands-on learning environment for post-quantum cryptography (PQC). Run real NIST-standardized algorithms, simulate the quantum attacks that motivate them, and explore how lattice-based cryptography works — all in Python, with no quantum hardware required.

## Why This Exists

Classical public-key cryptography (RSA, Diffie-Hellman, ECDSA) will be broken by a sufficiently large quantum computer running **Shor's algorithm**. NIST has standardized new algorithms to resist this threat:

| Standard | Algorithm Family | Purpose | Playground Example |
|----------|-----------------|---------|-------------------|
| [FIPS 203](https://csrc.nist.gov/pubs/fips/203/final) | ML-KEM (Kyber) | Key encapsulation | `examples/01_ml_kem_keygen.py` |
| [FIPS 204](https://csrc.nist.gov/pubs/fips/204/final) | ML-DSA (Dilithium) | Digital signatures | `examples/02_ml_dsa_signatures.py` |

This playground lets you run these algorithms, see their outputs, and understand what they do — without needing a PhD in lattice theory.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/thehhugg/quantum-resistant-encryption-playground.git
cd quantum-resistant-encryption-playground

# Install dependencies
pip install -r requirements.txt

# Run the ML-KEM (Kyber) key encapsulation demo
python examples/01_ml_kem_keygen.py

# Run the ML-DSA (Dilithium) digital signature demo
python examples/02_ml_dsa_signatures.py

# Simulate Grover's search algorithm
python quantum/grovers_simulation.py

# Simulate Shor's factoring algorithm
python quantum/shors_simulation.py
```

## What's Inside

### `examples/` — Post-Quantum Cryptography

Working demonstrations of NIST-standardized post-quantum algorithms.

**`01_ml_kem_keygen.py`** — ML-KEM (Kyber) key encapsulation. Generates keys, encapsulates a shared secret, and decapsulates it. Runs all three parameter sets (ML-KEM-512, 768, 1024) and reports key sizes, ciphertext sizes, and timing.

**`02_ml_dsa_signatures.py`** — ML-DSA (Dilithium) digital signatures. Generates signing keys, signs a message, verifies the signature, and demonstrates tamper detection. Runs all three parameter sets (ML-DSA-44, 65, 87).

### `quantum/` — Quantum Algorithm Simulations

Educational simulations of the quantum algorithms that threaten classical cryptography. Built with NumPy — no Qiskit or quantum hardware needed.

**`grovers_simulation.py`** — Grover's search algorithm. Shows how a quantum computer can search an unsorted space in O(sqrt(N)) time, which halves the effective key length of symmetric ciphers like AES. Configurable qubit count and target state. Generates a probability distribution chart.

```bash
python quantum/grovers_simulation.py --qubits 4 --target 7
```

**`shors_simulation.py`** — Shor's factoring algorithm. Demonstrates the algorithm that breaks RSA by factoring integers in polynomial time. Includes the full pipeline: classical reduction, simulated quantum period-finding, and continued fraction post-processing.

```bash
python quantum/shors_simulation.py --number 91 --verbose
```

### `ai/` — Performance Analysis

Machine learning models that analyze encryption performance data. These scripts use linear regression to predict encryption times based on lattice parameters.

**`lattice_optimizer.py`** — Multi-feature regression model predicting encryption time from lattice size, key generation time, and decryption time.

**`parameter_optimization.py`** — Single-feature regression model predicting encryption time from lattice size, with visualization.

### `data/` — Sample Data

**`encryption_times.csv`** — Sample performance measurements for lattice-based encryption at different parameter sizes.

### `scripts/` — Utilities

**`download_kyber.py`** — Optional script to clone the official Kyber C reference implementation. Most users do not need this; the Python examples use `kyber-py` instead.

## Project Structure

```
quantum-resistant-encryption-playground/
├── examples/
│   ├── 01_ml_kem_keygen.py          # ML-KEM key encapsulation demo
│   └── 02_ml_dsa_signatures.py      # ML-DSA digital signature demo
├── quantum/
│   ├── grovers_simulation.py        # Grover's search algorithm
│   └── shors_simulation.py          # Shor's factoring algorithm
├── ai/
│   ├── lattice_optimizer.py         # Multi-feature performance model
│   ├── parameter_optimization.py    # Single-feature performance model
│   └── utils/
│       └── data_handler.py          # CSV data loading utilities
├── data/
│   └── encryption_times.csv         # Sample performance data
├── scripts/
│   └── download_kyber.py            # Optional: clone Kyber C reference
├── requirements.txt
├── LICENSE
└── README.md
```

## Requirements

- Python 3.9+
- Dependencies are listed in `requirements.txt`:
  - `numpy`, `scipy`, `scikit-learn`, `matplotlib`, `pandas` — numerical computing and visualization
  - `kyber-py` — pure-Python ML-KEM implementation (educational)
  - `dilithium-py` — pure-Python ML-DSA implementation (educational)

Install everything with:

```bash
pip install -r requirements.txt
```

## Important Disclaimer

The cryptographic implementations used in this playground (`kyber-py`, `dilithium-py`) are **educational, not production-grade**. They are not constant-time and must not be used to protect real data. For production use, see [liboqs](https://github.com/open-quantum-safe/liboqs) or your language's official PQC library.

## Learning Path

If you are new to post-quantum cryptography, here is a suggested order:

1. **Start with Shor's** (`quantum/shors_simulation.py --verbose`). Understand why classical crypto is threatened.
2. **Run Grover's** (`quantum/grovers_simulation.py`). See why symmetric key lengths need to double.
3. **Try ML-KEM** (`examples/01_ml_kem_keygen.py`). This is the replacement for Diffie-Hellman / RSA key exchange.
4. **Try ML-DSA** (`examples/02_ml_dsa_signatures.py`). This is the replacement for RSA / ECDSA signatures.
5. **Explore the AI analysis** (`ai/lattice_optimizer.py`). See how lattice parameters affect performance.

## Contributing

Contributions are welcome. Please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)
