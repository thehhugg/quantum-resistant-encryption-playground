# Contributing

Thank you for your interest in contributing to the Quantum-Resistant Encryption Playground. This document explains how to get started.

## Getting Started

1. Fork the repository and clone your fork:

```bash
git clone https://github.com/<your-username>/quantum-resistant-encryption-playground.git
cd quantum-resistant-encryption-playground
```

2. Install the project with dev dependencies:

```bash
pip install -e ".[dev]"
```

3. Run the tests to make sure everything works:

```bash
make test
```

## Making Changes

1. Create a branch for your change:

```bash
git checkout -b your-feature-name
```

2. Make your changes. Follow the existing code style:
   - Use docstrings on all functions and modules.
   - Add educational comments explaining *why*, not just *what*.
   - Include type hints on function signatures.

3. Run the tests and linter before committing:

```bash
make test
make lint
```

4. Commit with a clear message describing what changed and why.

5. Push your branch and open a pull request against `main`.

## What We Are Looking For

Good contributions for this project include:

- **New PQC algorithm examples** (e.g., SLH-DSA/SPHINCS+, HQC, FrodoKEM)
- **New quantum algorithm simulations** (e.g., BB84 QKD, quantum teleportation)
- **Improved educational content** (better explanations, diagrams, tutorials)
- **Bug fixes** and **test coverage improvements**
- **Performance benchmarks** on different hardware

## Guidelines

- **Open an issue first** before starting significant work. This avoids duplicate effort and lets us discuss the approach.
- **Keep examples educational.** The goal is to teach, not to build production software. Prefer clarity over cleverness.
- **Do not use production crypto libraries** in examples unless comparing against them. The point is to show how the algorithms work, not to wrap existing libraries.
- **Add tests** for any new functionality.
- **Do not commit generated files** (charts, compiled bytecode, etc.). These are in `.gitignore`.

## Code of Conduct

Be respectful and constructive. This is an educational project and contributors of all experience levels are welcome.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
