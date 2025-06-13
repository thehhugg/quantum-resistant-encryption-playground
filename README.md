# Quantum-Resistant Encryption Playground

This repository collects small experiments around post-quantum cryptography and simple quantum algorithms. It bundles
machine learning utilities for analyzing encryption performance, a minimal quantum circuit example, and helper scripts
for working with the [Kyber](https://www.pq-crystals.org/kyber/) key encapsulation mechanism.

## Repository layout

```
.
├── ai/                  # Machine learning utilities for lattice-based schemes
│   ├── lattice_optimizer.py
│   ├── parameter_optimization.py
│   └── utils/
├── data/                # Example benchmark data
│   └── encryption_times.csv
├── kyber/               # Placeholder for the Kyber reference implementation
├── quantum/             # Simple quantum circuit example (Grover's)
├── scripts/             # Helper scripts such as Kyber downloader
└── requirements.txt     # Python dependencies
```

### `ai/`
* `parameter_optimization.py` – Demonstrates linear regression on synthetic lattice sizes and encryption times.
* `lattice_optimizer.py` – Loads `data/encryption_times.csv` and trains a regression model to predict encryption time.
* `utils/data_handler.py` – Small helpers for loading and saving CSV files.

### `quantum/`
* `grovers_simulation.py` – Uses Qiskit to build a two-qubit Grover circuit and prints its unitary matrix.

### `kyber/`
The Kyber implementation is **not** bundled in the repository. Use the helper script to download it:

```bash
python scripts/download_kyber.py
```

or manually clone the official repo into `kyber/`.

## Setup
1. Create a virtual environment (optional but recommended).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) run the Kyber download step above.

## Usage
Examples can be executed directly with Python:

```bash
# Predict encryption time for a specific lattice size
python ai/parameter_optimization.py

# Use real benchmark data and visualize the model
python ai/lattice_optimizer.py

# Run a small Grover's algorithm simulation
python quantum/grovers_simulation.py
```

The provided `data/encryption_times.csv` contains sample performance measurements with columns `lattice_size`,
`encryption_time`, `keygen_time` and `decryption_time`.

## Contributing
Pull requests are welcome for additional experiments or improvements. Feel free to open issues to discuss ideas or
questions about the playground.

## License
This repository is intended for educational purposes. The Kyber implementation retains its original license in the
`kyber/` directory. Other code in this repository is provided under the MIT License.
