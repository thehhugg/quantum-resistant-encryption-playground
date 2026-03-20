# Examples

Hands-on scripts that demonstrate post-quantum cryptography concepts. Each example is self-contained and can be run independently.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run any example
python examples/01_ml_kem_keygen.py
```

Or use the Makefile shortcuts:

```bash
make demo-kem       # ML-KEM key encapsulation
make demo-dsa       # ML-DSA digital signatures
make demo-compare   # Classical vs. PQC comparison
make demo-all       # Run everything
```

## Examples

| # | Script | What It Demonstrates |
|---|--------|---------------------|
| 01 | `01_ml_kem_keygen.py` | ML-KEM (Kyber) key encapsulation at all three security levels (512, 768, 1024). Shows key generation, encapsulation, and decapsulation. |
| 02 | `02_ml_dsa_signatures.py` | ML-DSA (Dilithium) digital signatures at all three security levels. Shows key generation, signing, verification, and tamper detection. |
| 03 | `03_classical_vs_pqc.py` | Side-by-side comparison of classical (RSA, ECDSA, ECDH) and post-quantum algorithms. Benchmarks key sizes, ciphertext/signature sizes, and operation timing. |

## Suggested Learning Path

1. **Start with `01_ml_kem_keygen.py`** to understand how post-quantum key exchange works.
2. **Move to `02_ml_dsa_signatures.py`** to see how post-quantum digital signatures differ.
3. **Run `03_classical_vs_pqc.py`** to see the concrete trade-offs between classical and PQC.
4. **Explore `quantum/`** to understand *why* we need PQC (Grover's, Shor's, BB84).
5. **Run `ai/`** scripts to see how ML can analyze PQC performance data.

## Adding New Examples

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines. New examples should:

- Be numbered sequentially (e.g., `04_new_example.py`)
- Include a module-level docstring explaining the concept
- Be runnable with `python examples/XX_name.py`
- Require only the dependencies in `requirements.txt`
